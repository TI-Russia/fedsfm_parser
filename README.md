# fedsfm_parser

## Arguments

`--data` — Required, `str`. Path to .xlsx table, wich shuld contain fields "ИНН" and "Регионы". We used ["Контур.Фокус"](https://focus.kontur.ru) dumps.

`--out` — Optional, `str`. Path to output directory. Default `"./"`.

`--okved` — Optional, `str`. "ОКВЕД" code for metadata. Default `"68:31"`.

## Output

As result parser generates a table `"done_rosfinmonitor.xlsx"` with two sheets: 1) **data** wich is simply input data with additional field `"реестр_Росфинмониторинга"` 2) **meta** wich descripts the resutl. And a log file `"rosfinmonitor.log"`. The log file may contain information about response errors (time to time ["Росфинмониторинг"](https://portal.fedsfm.ru/check-inn)  doesn't work correct) if so сheck these "ИНН" codes manually.

## NB

This parser uses selenium. It has never been used id headless mode, so GUI is required.
