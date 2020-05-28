from selenium.webdriver import Chrome
import os
import pandas as pd
from pandas import ExcelWriter
import re
import time
import random
from tqdm import tqdm
from comm import args
from datetime import datetime
import logging


if __name__ == '__main__':

    FORMATTER = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    LOG_FILE = os.path.join(args.out, "rosfinmonitor.log")

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(FORMATTER)

    e_logger = logging.getLogger("inn_error")
    e_logger.addHandler(file_handler)
    e_logger.setLevel(logging.ERROR)

    driver = Chrome("../chromedriver")

    driver.get("https://portal.fedsfm.ru/check-inn")
    time.sleep(random.uniform(5.5, 7.5))

    df = pd.read_excel(args.data, dtype=str)

    exs_j = {}

    with tqdm(total=df.shape[0]) as pbar:
        for i, r in df[:10].iterrows():

            if len(r["ИНН"]) == 10 or len(r["ИНН"]) == 12:
            
                try:

                    search = driver.find_element_by_id('innText')
                    search.send_keys(r["ИНН"])

                    btn = driver.find_element_by_id('checkInnButton')
                    btn.click()

                    time.sleep(random.uniform(1.5, 2.5))

                    success = driver.find_element_by_id('successCheck')
                    f = success.get_attribute("style") == "display: none;"

                    btn = driver.find_elements_by_class_name('btn.btn-primary.refreshButton.m-t.full-width')

                    if not f:
                        df.loc[i,"реестр_Росфинмониторинга"] = "1"
                        btn[0].click()

                    else:
                        df.loc[i,"реестр_Росфинмониторинга"] = "0"
                        btn[1].click()

                except Exception as E:

                    e_logger.error(" id: %s | inn: %s | %s", i, r["ИНН"], E)

                    driver.refresh()
                    time.sleep(random.uniform(7.5, 12.5))

                pbar.update()

    driver.quit()

    df = df.fillna("").astype(str)

    meta_df = pd.DataFrame(
        index=[
            "Дата загрузки",
            "Основной ОКВЭД",
            "Зарегистрированы код-1",
            "Не зарегистрированы код-0",
            "Нет результата",
            "Дубли ИНН",
            "Регионы"
        ]
    )

    meta_df.loc["Дата загрузки", 0] = datetime.strftime(datetime.now(), "%d.%m.%Y")
    meta_df.loc["Основной ОКВЭД", 0] = args.okved
    meta_df.loc["Зарегистрированы код-1", 0] = str(df[df["реестр_Росфинмониторинга"]=="1"].shape[0])
    meta_df.loc["Не зарегистрированы код-0", 0] = str(df[df["реестр_Росфинмониторинга"]=="0"].shape[0])
    meta_df.loc["Нет результата", 0] = str(df[df["реестр_Росфинмониторинга"]==""].shape[0])
    meta_df.loc["Дубли ИНН", 0] = str(df[df.duplicated("ИНН")].shape[0])
    meta_df.loc["Регионы", 0] = ", ".join(df["Регион регистрации"].drop_duplicates().values)

    with ExcelWriter(os.path.join(args.out, "done_rosfinmonitor.xlsx"), engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='data', index=False)
        meta_df.to_excel(writer, sheet_name='meta', header=False)

