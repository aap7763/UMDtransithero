# Shared contracts

This directory is the single source of truth for JSON shapes shared by the
frontend, backend, and data integration. Files use JSON Schema Draft 2020-12;
each includes examples. Resolve `$ref` paths relative to the containing schema
and reuse the shared definitions instead of copying fields into new contracts.

| Schema | Producer → consumer | Shape |
|--------|---------------------|-------|
| `ask-request.schema.json` | `frontend/index.html` → `backend/main.py`, `POST /api/v1/ask` | Object with a plain-English `question` |
| `ask-response.schema.json` | `backend/main.py` → frontend, successful `POST /api/v1/ask` | Object with `answer` and `buses` |
| `transit-request.schema.json` | `backend/ai.py` → `backend/main.py` → `backend/transit.py` | Parsed object with `stop`; main passes the field as `get_next_buses(stop_name)` |
| `transit-response.schema.json` | `backend/transit.py` → backend AI and frontend | Array of normalized upcoming-bus records |
| `bus.schema.json` | Data integration / transit logic → shared consumers | One arrival: string `route`, string `stop`, nonnegative integer `arrives_in_min` |
| `error.schema.json` | Backend → frontend, unsuccessful API requests | Object with `error.code` and `error.message` |

## Conventions

- The API base path is `/api/v1`. `/ask` remains a compatibility alias for
  `/api/v1/ask`; new clients should use the versioned path.
- Requests and responses use JSON (`Content-Type: application/json`).
- Timestamps must use ISO 8601 with an explicit offset, for example
  `2026-10-25T15:20:00-04:00`. The current payloads have no timestamp fields;
  `arrives_in_min` is a duration, not a timestamp.
- IDs are GTFS IDs represented as strings. The current `route` field is a
  display label and `stop` is a name, not an ID; do not substitute them for
  `route_id` or `stop_id` when adding ID-based lookups.
- Fields annotated with `"derived": true` are computed by the backend, not
  read directly from GTFS. This is a documentation annotation, not a standard
  JSON Schema validation keyword.
- All errors use `error.schema.json` with an appropriate non-2xx HTTP status.
  The current HTTP error codes use uppercase names with underscores, such as
  `BAD_REQUEST`, `NOT_FOUND`, and `UNSUPPORTED_MEDIA_TYPE`. `STOP_NOT_FOUND`
  illustrates a future domain error; ID-based lookup is not implemented yet.

`POST /api/v1/ask` uses `Content-Type: application/json`. The question may be omitted;
the existing backend substitutes `""`. JSON Schema's `default` is documentation,
not an instruction for validators to insert a value. Empty bus arrays are valid.
The internal transit lookup is a function call, not a separate HTTP endpoint.

The transit implementation currently returns mock arrivals. When real files are
added to `data/`, the data integration should normalize their records into
`bus.schema.json` before returning them to consumers. These schemas do not define
raw GTFS files or invent a stored dataset format. Add a contract here when that
interface is implemented.

These contracts document the intended payloads; JSON Schema validation is not
automatically applied at runtime. The server checks that the request is a JSON
object and that `question`, if supplied, is a string, and returns shared JSON
errors for invalid requests and HTTP errors.
Coordinate contract changes across affected producers and consumers in the same
change, and update examples alongside the schemas.
