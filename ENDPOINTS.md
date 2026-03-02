# API Endpoints

All successful responses follow the envelope:

```json
{
  "success": true,
  "data": { ... }
}
```

All error responses follow the envelope:

```json
{
  "success": false,
  "error": "<message>"
}
```

---

## Wells

### `GET /well`

Returns a list of all wells.

**Response `data`:**
```json
{
  "wells": [
    {
      "inline": 100,
      "crossline": 200,
      "x": 407890.049,
      "y": 1234567.89,
      "trace_number": 42,
      "bottom": -3200.0,
      "bottom_reff": -3150.0,
      "top": -2800.0,
      "top_reff": -2750.0,
      "well_x": 407890.049,
      "well_y": 1234567.89,
      "well_name": "WELL-01",
      "distance": 123.45
    }
  ],
  "count": 1
}
```

---

### `GET /well/summary`

Returns summary statistics across all wells.

**Response `data`:**
```json
{
  "total_wells": 25,
  "statistics": {
    "inline": {
      "min": 100,
      "max": 500,
      "range": 400
    },
    "crossline": {
      "min": 200,
      "max": 600,
      "range": 400
    }
  },
  "well_names": ["WELL-01", "WELL-02"]
}
```

---

### `GET /well/<well_name>`

Returns the data for a single well by name.

**Path parameter:** `well_name` — name of the well (string)

**Response `data`:**
```json
{
  "inline": 100,
  "crossline": 200,
  "x": 407890.049,
  "y": 1234567.89,
  "trace_number": 42,
  "bottom": -3200.0,
  "bottom_reff": -3150.0,
  "top": -2800.0,
  "top_reff": -2750.0,
  "well_x": 407890.049,
  "well_y": 1234567.89,
  "well_name": "WELL-01",
  "distance": 123.45
}
```

**Error responses:**
- `404` — well not found
- `400` — invalid request

---

### `GET /well/<well_name>/exists`

Checks whether a well with the given name exists.

**Path parameter:** `well_name` — name of the well (string)

**Response `data`:**
```json
{
  "exists": true
}
```

---

## Well Logs

Well logs are grouped by log type:
- `phie`
- `swe`
- `vsh`

For every type, available endpoints are:
- `GET /well-log/<log_type>`
- `GET /well-log/<log_type>/wells`
- `GET /well-log/<log_type>/<well_name>`

Empty values in CSV are returned as `null`.

---

### `GET /well-log/phie`

Returns PHIE logs for all wells.

**Response `data`:**
```json
{
  "wells": [
    {
      "well_name": "MJ-106",
      "log_type": "phie",
      "entries": [
        { "twt": 0.0, "value": null },
        { "twt": -2.0, "value": null },
        { "twt": -128.0, "value": 0.001351232 }
      ],
      "count": 2500
    }
  ],
  "count": 26
}
```

---

### `GET /well-log/phie/wells`

Returns list of available well names in PHIE.

**Response `data`:**
```json
{
  "well_names": ["MJ-106", "MJ-115", "MJ-116"],
  "count": 26
}
```

---

### `GET /well-log/phie/<well_name>`

Returns PHIE log entries for one well.

**Path parameter:** `well_name` — name of the well (string)

**Response `data`:**
```json
{
  "well_name": "MJ-106",
  "log_type": "phie",
  "entries": [
    { "twt": 0.0, "value": null },
    { "twt": -2.0, "value": null },
    { "twt": -128.0, "value": 0.001351232 }
  ],
  "count": 2500
}
```

**Error responses:**
- `404` — well not found in PHIE log

---

### `GET /well-log/swe`

Returns SWE logs for all wells.

---

### `GET /well-log/swe/wells`

Returns list of available well names in SWE.

---

### `GET /well-log/swe/<well_name>`

Returns SWE log entries for one well.

**Error responses:**
- `404` — well not found in SWE log

---

### `GET /well-log/vsh`

Returns VSH logs for all wells.

---

### `GET /well-log/vsh/wells`

Returns list of available well names in VSH.

---

### `GET /well-log/vsh/<well_name>`

Returns VSH log entries for one well.

**Error responses:**
- `404` — well not found in VSH log

---

## Horizons

### `GET /horizon`

Returns all horizon data points.

**Response `data`:**
```json
{
  "horizons": [
    {
      "X": 407890,
      "Y": 1234567,
      "Inline": 100,
      "Crossline": 200,
      "TraceNumber": 42,
      "bottom": -3200.0,
      "bottom_reff": -3150.0,
      "top": -2800.0,
      "top_reff": -2750.0
    }
  ],
  "count": 1
}
```

---

### `GET /horizon-page`

Returns a paginated list of horizon data points.

**Query parameters:**

| Parameter   | Type | Default | Description          |
|-------------|------|---------|----------------------|
| `page`      | int  | `1`     | Page number          |
| `page_size` | int  | `500`   | Number of items per page |

**Response `data`:** *(same shape as `GET /horizon`)*

---

## Seismic Sections

### `GET /inline/<number>/image`

Returns a PNG image of the requested inline seismic section.

**Path parameter:** `number` — inline section number (integer)

**Response:** Binary PNG image (`Content-Type: image/png`)

**Error responses:**
- `404` — inline section not found

---

### `GET /crossline/<number>/image`

Returns a PNG image of the requested crossline seismic section.

**Path parameter:** `number` — crossline section number (integer)

**Response:** Binary PNG image (`Content-Type: image/png`)

**Error responses:**
- `404` — crossline section not found
