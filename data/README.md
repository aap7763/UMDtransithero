Put the bus files here (GTFS, schedules, JSON, etc).

Shared JSON shapes are defined in [`../contract/`](../contract/README.md).
When implementing data loading, normalize upcoming arrivals to
`bus.schema.json` and return them as `transit-response.schema.json`.
Raw source files may keep their native format; the contracts describe the
normalized interface consumed by the backend and frontend.
