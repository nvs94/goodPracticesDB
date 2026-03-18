# config.yaml - ejemplo de configuración para entornos pre y pro

key-vault:
  pre: 
    tm: "kv-aq-awa-tm-cont-pre-01"
    shared: "kv-aq-awa-sh-pre-01"
  pro: 
    tm: "kv-aq-awa-tm-cont-pro-01"
    shared: "kv-aq-awa-sh-pro-01"

elastic:
  pre:
    sdg:
      es_nodes: "https://pre-fcc-aqualia-sa-metrics-analytics.es.eu-west-1.aws.found.io"
      es_username: "azure-telemetry"
    aqualia:
      es_nodes: "https://7ab6c0feb872458f90b7b80898514f72.eu-west-1.aws.found.io"
      es_x_found_cluster: "dea5c7ae944d4a71b7d2f9cdc09d10a3"
      es_username: "Sdg_Elastic"
  pro:
    sdg:
      es_nodes: "https://dea5c7ae944d4a71b7d2f9cdc09d10a3.eu-west-1.aws.found.io"
      es_username: "azure-telemetry"
    aqualia:
      es_nodes: "https://7ab6c0feb872458f90b7b80898514f72.eu-west-1.aws.found.io"
      es_x_found_cluster: "dea5c7ae944d4a71b7d2f9cdc09d10a3"
      es_username: "Sdg_Elastic"

sql-server:
  pre:
    host: "sql-aq-awa-dw-pre-01.database.windows.net"
    port: "1433"
    database: "sqldb-aq-awa-dw-pre-01"
    schema: "telemedida"
  pro:
    host: "sql-aq-awa-dw-pro-01.database.windows.net"
    port: "1433"
    database: "sqldb-aq-awa-dw-pro-01"
    schema: "telemedida"
