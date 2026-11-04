# Evidencias del laboratorio 2 versión 2.1

Participante: Daniela Bugeda  Fecha: 29 octubre 2026

No incluyas claves, tokens ni datos recuperados. Escribe los resultados observados, no solo los esperados.

## Preparación y comprobaciones

Resultado de comprobar_preparacion_lab2.py: 

Preparacion verificada: datos, referencia, clave y TODO 1 a 4
No se han creado salidas ni mostrado claves o datos personales

Resultado de comprobar_lab2.py --todo 5: 

TODO 5 OK: tres eventos anexados con campos exactos y fecha UTC.
Etapa TODO 5 verificada; no valida las otras funciones.

Resultado de comprobar_lab2.py --todo 6: 

TODO 6 OK: resumen valido aceptado y ocho casos invalidos rechazados.
Etapa TODO 6 verificada; no valida las otras funciones.

Resultado de comprobar_lab2.py --todo 7: 

TODO 7 OK: traza valida aceptada y catorce casos invalidos rechazados.
Etapa TODO 7 verificada; no valida las otras funciones.

Resultado de comprobar_lab2.py completo: 

TODO 5 OK: tres eventos anexados con campos exactos y fecha UTC.
TODO 6 OK: resumen valido aceptado y ocho casos invalidos rechazados.
TODO 7 OK: traza valida aceptada y catorce casos invalidos rechazados.
TODO 5, 6 y 7 verificados. Continua con la auditoria completa.

## Auditoría válida

RUN_ID: 3ce7d7486dcc4c3f945ea37583fc0a02

Ruta de reporte.json: ejecuciones/3ce7d7486dcc4c3f945ea37583fc0a02/reporte.json

Ruta de eventos.jsonl: ejecuciones/3ce7d7486dcc4c3f945ea37583fc0a02/eventos.jsonl

| Control | Estado observado | Evidencia concreta |
| --- | --- | --- |
| INTEGRIDAD | SATISFACTORIO | hash_entrada del reporte |
| CIFRADO | SATISFACTORIO | alidas/detalle_protegido.csv |
| MINIMIZACION | SATISFACTORIO | salidas/resumen.csv |
| ACCESO_DENEGADO | SATISFACTORIO | eventos.jsonl |
| TRAZABILIDAD | SATISFACTORIO | eventos.jsonl |

Filas de detalle: 13  Filas de resumen: 4

Totales por ciudad y total general: 

Merida,4000.00
Puebla,2500.00
Villahermosa,4250.00
Total General,10750.00

## Escenarios negativos

| Escenario | RUN_ID o ruta | Estados y resultado observados | Acción propuesta |
| --- | --- | --- | --- |
| A Entrada alterada |ejecuciones/d1ae8500742b44c7950d912e1c49e617 | INTEGRIDAD y EJECUCION **FALLIDO**; CIFRADO, MINIMIZACION, ACCESO_DENEGADO y TRAZABILIDAD **NO_EVALUADO** | |
| B Analista intenta ejecutar | ejecuciones/ef614c78c997432eb79f9a99d43ab9ef|AUTORIZACION_INICIAL y EJECUCION **FALLIDO**, el resto **NO_EVALUADO** | |
| C Analista intenta consultar | No genera RUN_ID | PermissionError('Operacion no autorizada para el rol') | |
| D Pruebas aisladas | Archivos temporales | | |

¿Se crearon salidas del pipeline en A o B? ____________________

¿Qué controles quedaron NO_EVALUADO y por qué? ____________________

## Hallazgo y explicación

Qué ocurrió: ____________________

Qué control actuó: ____________________

Dónde está la evidencia: ____________________

Qué corregirías: ____________________

Qué no demuestra este laboratorio: ____________________
