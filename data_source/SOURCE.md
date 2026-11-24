# Data source

**Catálogo Nacional de Códigos Postales**, published for free by Correos de México.
Official download page: https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx

The same catalog comes in three formats. All of them hold exactly the same 159,527 rows and 15 columns:

| File | Format | Size | In this repo? |
|---|---|---|---|
| `CPdescarga.txt` | pipe-separated text, Latin-1 | about 15 MB | Yes (this is the one our code reads) |
| `CPdescarga.xml` | XML | about 67 MB | No, too big for GitHub's web upload |
| `CPdescarga.xls` | Excel (legacy) | about 72 MB | No, too big for GitHub's web upload |

If you need the XML or the XLS, download them again from the official page above.

## Columns we use
`d_codigo` (postal code), `d_asenta` (neighborhood), `d_tipo_asenta` (type), `D_mnpio` (municipality),
`d_estado` (state), `d_ciudad` (city), `d_zona` (urban, rural or semiurban).

## Quick facts
159,527 rows, 31,860 distinct postal codes, 32 states, 2,478 municipalities, no duplicate rows.

## License note
Correos de México provides the catalog for private use and does not allow commercial use or redistribution to third parties.
Keep this repository **private** and share it only with the members of Group 11.
