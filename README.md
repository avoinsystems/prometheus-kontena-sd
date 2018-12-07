prometheus-kontena-sd
=====================

`prometheus-kontena-sd` is a super-ugly [file-based service discovery](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#%3Cfile_sd_config%3E)
tool for reading the service IP addresses from etcd managed by [Kontena Classic](https://www.kontena.io/classic).

By default it reads hosts from etcd (directory: `/kontena/ipam/addresses/kontena`) every 5 minutes, tries to connect
to `http://host:port/metrics` and if HTTP 200 is returned, the host gets added to a JSON file
`/discovery/kontena_sd.json` from the output. This file should be placed inside a volume shared
by Prometheus and `prometheus-kontena-sd`.

Environment variables:
 - `ADDRESS_PATH`: the source etcd path where to read the hosts from
 - `FILE_SD_PATH`: the destination JSON-formatted service discovery file
 - `SLEEP_TIME`: refresh rate for generating the file in seconds
 - `PORTS`: a comma-separated list of ports that the tool tries to connect to
