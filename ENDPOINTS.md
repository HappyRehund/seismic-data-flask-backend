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
      "inline_n": 1,
      "crossline_n": 1,
      "x": 407890.049,
      "y": 1234567.89,
      "trace_number": 42,
      "basement": -3200.0,
      "basement_reff": -3150.0,
      "surface": 0.0,
      "surface_reff": 10.0,
      "well_x": 407890.049,
      "well_y": 1234567.89,
      "well_name": "WELL-01"
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
  "inline_n": 1,
  "crossline_n": 1,
  "x": 407890.049,
  "y": 1234567.89,
  "trace_number": 42,
  "basement": -3200.0,
  "basement_reff": -3150.0,
  "surface": 0.0,
  "surface_reff": 10.0,
  "well_x": 407890.049,
  "well_y": 1234567.89,
  "well_name": "WELL-01"
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

### `GET /well-log`

Returns all well log entries.

**Response `data`:**
```json
{
  "well_logs": [
    {
      "id": "abc123",
      "well": "WELL-01",
      "depth": 1000.0,
      "tvdss": -980.0,
      "xcoord": 407890.049,
      "ycoord": 1234567.89,
      "gr": 75.3,
      "rt": 12.5,
      "rhob": 2.45,
      "nphi": 0.22,
      "dt": 68.0,
      "dts": 115.0,
      "dtst": 0.0,
      "sp": -40.0,
      "phie": 0.18,
      "phit": 0.20,
      "vsh": 0.30,
      "swe": 0.55,
      "rwa": 0.01,
      "iqual": 1.0,
      "litho": 2.0,
      "fluid": 1.0,
      "m": 2.0,
      "n": 2.0,
      "zone": 3.0,
      "marker": 0.0,
      "fa_status": 1.0
    }
  ],
  "count": 1
}
```

---

### `GET /well-log-page`

Returns a paginated list of well log entries.

**Query parameters:**

| Parameter   | Type | Default | Description          |
|-------------|------|---------|----------------------|
| `page`      | int  | `1`     | Page number          |
| `page_size` | int  | `500`   | Number of items per page |

**Response `data`:** *(same shape as `GET /well-log`)*

---

### `GET /well-log/<well_name>`

Returns all well log entries for a specific well.

**Path parameter:** `well_name` — name of the well (string)

**Response `data`:** *(same shape as `GET /well-log`)*

**Error responses:**
- `404` — no well logs found for the given well name

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
