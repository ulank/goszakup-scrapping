from io import BytesIO
from fastapi.responses import StreamingResponse
import scrapping.util as scrapping
import pandas as pandas
from fastapi import FastAPI

app = FastAPI()


@app.get("/get-xlsx/goszakup/suppliers/max-records")
async def get_xlsx_goszakup():
    suppliers = scrapping.goszakup_scrapping_all_suppliers('https://www.goszakup.gov.kz/ru/registry/rqc?count_record'
                                                           '=2000', False)
    data_frame = pandas.json_normalize(suppliers)
    buffer = BytesIO()
    with pandas.ExcelWriter(buffer) as writer:
        data_frame.to_excel(writer, index=False)
    return StreamingResponse(
        BytesIO(buffer.getvalue()),
        media_type='multipart/form-data',
        headers={"Content-Disposition": f"attachment; filename=goszakup.xlsx"})
