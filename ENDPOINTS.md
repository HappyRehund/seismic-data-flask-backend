# API Endpoints

All endpoints are served under the `/api` prefix (e.g., `http://localhost:5000/api/well`).

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

## Dataset Selection

Most modules support selecting a specific dataset via the `?dataset=` query parameter.
If omitted, each module uses its own default dataset.

To discover available datasets for any module, use its `/datasets` endpoint:

| Module | Endpoint |
|---|---|
| Horizon | `GET /api/horizon/datasets` |
| Seismic | `GET /api/seismic/datasets` |
| Image Helper | `GET /api/image-helper/datasets` |
| Well | `GET /api/well/datasets` |
| Well Log | `GET /api/well-log/datasets` |

---

## Wells

### `GET /api/well/datasets`

Returns available well datasets.

**Response `data`:**
```json
{
  "datasets": ["well_coordinatesmj_B_G"],
  "count": 1
}
```

**Test:**
```bash
curl http://localhost:5000/api/well/datasets
```

---

### `GET /api/well`

Returns a list of all wells.

**Query parameters:**

| Parameter  | Type   | Default                    | Description        |
|------------|--------|----------------------------|--------------------|
| `dataset`  | string | `well_coordinatesmj_B_G`   | Dataset name       |

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

**Test:**
```bash
# Default dataset
curl http://localhost:5000/api/well

# Specific dataset
curl http://localhost:5000/api/well?dataset=well_coordinatesmj_B_G
```

---

### `GET /api/well/summary`

Returns summary statistics across all wells.

**Query parameters:**

| Parameter  | Type   | Default                    | Description        |
|------------|--------|----------------------------|--------------------|
| `dataset`  | string | `well_coordinatesmj_B_G`   | Dataset name       |

**Response `data`:**
```json
{
  "total_wells": 25,
  "statistics": {
    "inline": { "min": 100, "max": 500, "range": 400 },
    "crossline": { "min": 200, "max": 600, "range": 400 }
  },
  "well_names": ["WELL-01", "WELL-02"]
}
```

**Test:**
```bash
curl http://localhost:5000/api/well/summary
```

---

### `GET /api/well/<well_name>`

Returns the data for a single well by name.

**Path parameter:** `well_name` — name of the well (string)

**Query parameters:**

| Parameter  | Type   | Default                    | Description        |
|------------|--------|----------------------------|--------------------|
| `dataset`  | string | `well_coordinatesmj_B_G`   | Dataset name       |

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

**Test:**
```bash
curl http://localhost:5000/api/well/MJ-106
```

---

### `GET /api/well/<well_name>/exists`

Checks whether a well with the given name exists.

**Path parameter:** `well_name` — name of the well (string)

**Query parameters:**

| Parameter  | Type   | Default                    | Description        |
|------------|--------|----------------------------|--------------------|
| `dataset`  | string | `well_coordinatesmj_B_G`   | Dataset name       |

**Response `data`:**
```json
{
  "exists": true
}
```

**Test:**
```bash
curl http://localhost:5000/api/well/MJ-106/exists
```

---

## Well Logs

Well logs are grouped by log type:
- `phie`
- `swe`
- `vsh`

For every type, available endpoints are:
- `GET /api/well-log/<log_type>`
- `GET /api/well-log/<log_type>/wells`
- `GET /api/well-log/<log_type>/<well_name>`

Empty values in CSV are returned as `null`.

### `GET /api/well-log/datasets`

Returns available well-log datasets and their log types.

**Response `data`:**
```json
{
  "datasets": {
    "default": ["phie", "swe", "vsh"]
  },
  "count": 1
}
```

**Test:**
```bash
curl http://localhost:5000/api/well-log/datasets
```

---

### `GET /api/well-log/phie`

Returns PHIE logs for all wells.

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

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

**Test:**
```bash
# Default dataset
curl http://localhost:5000/api/well-log/phie

# Specific dataset
curl http://localhost:5000/api/well-log/phie?dataset=default
```

---

### `GET /api/well-log/phie/wells`

Returns list of available well names in PHIE.

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

**Response `data`:**
```json
{
  "well_names": ["MJ-106", "MJ-115", "MJ-116"],
  "count": 26
}
```

**Test:**
```bash
curl http://localhost:5000/api/well-log/phie/wells
```

---

### `GET /api/well-log/phie/<well_name>`

Returns PHIE log entries for one well.

**Path parameter:** `well_name` — name of the well (string)

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

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

**Test:**
```bash
curl http://localhost:5000/api/well-log/phie/MJ-106
```

---

### `GET /api/well-log/swe`

Returns SWE logs for all wells.

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

**Test:**
```bash
curl http://localhost:5000/api/well-log/swe
```

---

### `GET /api/well-log/swe/wells`

Returns list of available well names in SWE.

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

**Test:**
```bash
curl http://localhost:5000/api/well-log/swe/wells
```

---

### `GET /api/well-log/swe/<well_name>`

Returns SWE log entries for one well.

**Path parameter:** `well_name` — name of the well (string)

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

**Error responses:**
- `404` — well not found in SWE log

**Test:**
```bash
curl http://localhost:5000/api/well-log/swe/MJ-106
```

---

### `GET /api/well-log/vsh`

Returns VSH logs for all wells.

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

**Test:**
```bash
curl http://localhost:5000/api/well-log/vsh
```

---

### `GET /api/well-log/vsh/wells`

Returns list of available well names in VSH.

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

**Test:**
```bash
curl http://localhost:5000/api/well-log/vsh/wells
```

---

### `GET /api/well-log/vsh/<well_name>`

Returns VSH log entries for one well.

**Path parameter:** `well_name` — name of the well (string)

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

**Error responses:**
- `404` — well not found in VSH log

**Test:**
```bash
curl http://localhost:5000/api/well-log/vsh/MJ-106
```

---

## GNK Well Log

The GNK well log is a separate dataset from the geophysics team with a different schema (comprehensive log with GR, RT, RHOB, NPHI, etc.).

### `GET /api/well-log/gnk`

Returns all GNK well log entries.

**Response `data`:**
```json
{
  "entries": [
    {
      "id": "",
      "well": "GNK-052",
      "depth": 0.0,
      "tvdss": -19.03,
      "xcoord": 397912.589,
      "ycoord": 9625205.315,
      "gr": null,
      "rt": null,
      "rhob": null,
      "nphi": null,
      "dt": null,
      "dts": null,
      "dtst": null,
      "sp": null,
      "phie": null,
      "phit": null,
      "vsh": null,
      "swe": null,
      "swt": null,
      "rwa": null,
      "iqual": null,
      "litho": null,
      "fluid": null,
      "m": null,
      "n": null,
      "zone": null,
      "marker": null,
      "fa_status": null
    }
  ],
  "count": 934027
}
```

**Test:**
```bash
curl http://localhost:5000/api/well-log/gnk
```

---

### `GET /api/well-log/gnk/wells`

Returns list of available well names in the GNK well log.

**Response `data`:**
```json
{
  "well_names": ["GNK-052", "GNK-053", "GNK-055"],
  "count": 59
}
```

**Test:**
```bash
curl http://localhost:5000/api/well-log/gnk/wells
```

---

### `GET /api/well-log/gnk/<well_name>`

Returns GNK well log entries for one well.

**Path parameter:** `well_name` — name of the well (string)

**Response `data`:**
```json
{
  "entries": [ ... ],
  "count": 14831
}
```

**Error responses:**
- `404` — well not found in GNK well log

**Test:**
```bash
curl http://localhost:5000/api/well-log/gnk/GNK-052
```

---

### `GET /api/well-log/gnk/count`

Returns total entry count for the GNK well log.

**Response `data`:**
```json
{
  "total_entries": 934027
}
```

**Test:**
```bash
curl http://localhost:5000/api/well-log/gnk/count
```

---

## Horizons

### `GET /api/horizon/datasets`

Returns available horizon datasets.

**Response `data`:**
```json
{
  "datasets": ["MJ_MID_coords", "horizon"],
  "count": 2
}
```

**Test:**
```bash
curl http://localhost:5000/api/horizon/datasets
```

---

### `GET /api/horizon`

Returns all horizon data points.

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `horizon` | Dataset name       |

**Response `data`:**
```json
{
  "horizons": [
    {
      "X": 407890.0,
      "Y": 1234567.0,
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

**Test:**
```bash
# Default dataset
curl http://localhost:5000/api/horizon

# Specific dataset
curl http://localhost:5000/api/horizon?dataset=MJ_MID_coords
```

---

### `GET /api/horizon-page`

Returns a paginated list of horizon data points.

**Query parameters:**

| Parameter   | Type   | Default   | Description          |
|-------------|--------|-----------|----------------------|
| `page`      | int    | `1`       | Page number          |
| `page_size` | int    | `500`     | Number of items per page |
| `dataset`   | string | `horizon` | Dataset name         |

**Response `data`:** *(same shape as `GET /horizon`)*

**Test:**
```bash
# Default dataset, page 1
curl http://localhost:5000/api/horizon-page?page=1&page_size=100

# Specific dataset
curl http://localhost:5000/api/horizon-page?dataset=MJ_MID_coords&page=1&page_size=100
```

---

## Seismic Sections

### `GET /api/seismic/datasets`

Returns available seismic datasets and the section types available in each.

**Response `data`:**
```json
{
  "datasets": {
    "aster": ["crossline", "inline"],
    "default": ["crosslineMJB", "inlineMJB"]
  },
  "count": 2
}
```

**Test:**
```bash
curl http://localhost:5000/api/seismic/datasets
```

---

### `GET /api/inline/<number>/image`

Returns a PNG image of the requested inline seismic section.

**Path parameter:** `number` — inline section number (integer)

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

**Response:** Binary PNG image (`Content-Type: image/png`)

**Error responses:**
- `404` — inline section not found in dataset

**Test:**
```bash
# From the "aster" dataset
curl -o inline_1.png http://localhost:5000/api/inline/1/image?dataset=aster

# From the "default" dataset (returns 404 if inline not available)
curl -o inline_1.png http://localhost:5000/api/inline/1/image?dataset=default
```

---

### `GET /api/crossline/<number>/image`

Returns a PNG image of the requested crossline seismic section.

**Path parameter:** `number` — crossline section number (integer)

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

**Response:** Binary PNG image (`Content-Type: image/png`)

**Error responses:**
- `404` — crossline section not found in dataset

**Test:**
```bash
curl -o crossline_1.png http://localhost:5000/api/crossline/1/image?dataset=aster
```

---

### `GET /api/inlineMJB/<number>/image`

Returns a PNG image of the requested inline MJB seismic section.

**Path parameter:** `number` — inline MJB section number (integer)

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

**Response:** Binary PNG image (`Content-Type: image/png`)

**Error responses:**
- `404` — inline MJB section not found in dataset

**Test:**
```bash
curl -o inlineMJB_1.png http://localhost:5000/api/inlineMJB/1/image?dataset=default
```

---

### `GET /api/crosslineMJB/<number>/image`

Returns a PNG image of the requested crossline MJB seismic section.

**Path parameter:** `number` — crossline MJB section number (integer)

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

**Response:** Binary PNG image (`Content-Type: image/png`)

**Error responses:**
- `404` — crossline MJB section not found in dataset

**Test:**
```bash
curl -o crosslineMJB_1.png http://localhost:5000/api/crosslineMJB/1/image?dataset=default
```

---

## Image Helper

### `GET /api/image-helper/datasets`

Returns available image helper datasets and the section types available in each.

**Response `data`:**
```json
{
  "datasets": {
    "aster": ["crossline", "inline"],
    "default": ["crosslineMJB", "inlineMJB"]
  },
  "count": 2
}
```

**Test:**
```bash
curl http://localhost:5000/api/image-helper/datasets
```

---

### `GET /api/image-helper/<section_type>/<number>/dimensions`

Returns the dimensions (width, height) of a seismic section image without downloading the full image.

**Path parameters:**
- `section_type` — one of: `inline`, `crossline`, `inlineMJB`, `crosslineMJB`
- `number` — section number (integer)

**Query parameters:**

| Parameter  | Type   | Default   | Description        |
|------------|--------|-----------|--------------------|
| `dataset`  | string | `default` | Dataset name       |

**Response `data`:**
```json
{
  "section_type": "inline",
  "section_number": 1,
  "width": 2790,
  "height": 1386,
  "image_path": "/path/to/csv_data/inline_crossline/aster/inline/inline_1.png"
}
```

**Error responses:**
- `404` — image not found in dataset
- `400` — invalid section type or section number

**Test:**
```bash
# From the "aster" dataset
curl http://localhost:5000/api/image-helper/inline/1/dimensions?dataset=aster

# From the "default" dataset
curl http://localhost:5000/api/image-helper/inlineMJB/1/dimensions?dataset=default
```
