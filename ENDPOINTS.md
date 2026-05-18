# Seismic Viewer Backend API Documentation

> **Base URL:** `http://localhost:5000`
>
> **Authentication:** No authentication is required for any endpoint.

---

## Table of Contents

1. [Health Check](#health-check)
2. [Wells](#wells)
3. [Well Logs](#well-logs)
4. [GNK Well Logs](#gnk-well-logs)
5. [Horizons](#horizons)
6. [Image Helper](#image-helper)
7. [Seismic Sections](#seismic-sections)

---

## Response Format

All JSON endpoints return responses in the following standard envelope:

### Success Response

```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

### List Responses

List endpoints include both the items array and a `count` field inside `data`:

```json
{
  "success": true,
  "data": {
    "items": [ ... ],
    "count": 42
  }
}
```

> Note: The exact key name for the items array varies by endpoint (e.g., `"wells"`, `"horizons"`, `"well_names"`, `"entries"`).

---

## Health Check

### `GET /health`

**Purpose:** Verify that the backend service is running and responsive.

**Query Parameters:** None

**Example Request:**

```bash
curl http://localhost:5000/health
```

**Example Response:**

```json
{
  "status": "ok",
  "message": "Seismic Viewer Backend is running"
}
```

---

## Wells

Base path: `/api`

### `GET /api/well`

**Purpose:** Retrieve all well coordinates from a given dataset.

**Query Parameters:**

| Parameter | Type   | Default                  | Description                          |
|-----------|--------|--------------------------|--------------------------------------|
| `dataset` | string | `well_coordinatesmj_B_G` | Name of the well dataset to query.   |

**Example Request:**

```bash
# Using default dataset
curl http://localhost:5000/api/well

# Using a specific dataset
curl "http://localhost:5000/api/well?dataset=well_coordinatesmj_B_G"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "wells": [
      {
        "inline": 480,
        "crossline": 403,
        "x": 342769.13,
        "y": 9694230.8,
        "trace_number": 15033,
        "bottom": 590.0,
        "bottom_reff": 295.0,
        "top": 418.0,
        "top_reff": 209.0,
        "well_x": 342772.48,
        "well_y": 9694232.43,
        "well_name": "MJ-106",
        "distance": 3.725506676
      },
      {
        "inline": 425,
        "crossline": 480,
        "x": 342407.59,
        "y": 9695523.93,
        "trace_number": 5430,
        "bottom": 584.0,
        "bottom_reff": 292.0,
        "top": 410.0,
        "top_reff": 205.0,
        "well_x": 342413.2,
        "well_y": 9695518.6,
        "well_name": "MJ-115",
        "distance": 7.738281463
      }
    ],
    "count": 27
  }
}
```

**Error Response:**

```json
{
  "success": false,
  "error": "Dataset 'unknown_dataset' not found"
}
```
HTTP Status: `500`

---

### `GET /api/well/summary`

**Purpose:** Retrieve a summary of wells including total count, inline/crossline statistics, and a list of all well names.

**Query Parameters:**

| Parameter | Type   | Default                  | Description                          |
|-----------|--------|--------------------------|--------------------------------------|
| `dataset` | string | `well_coordinatesmj_B_G` | Name of the well dataset to query.   |

**Example Request:**

```bash
curl http://localhost:5000/api/well/summary
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "total_wells": 27,
    "statistics": {
      "inline": {
        "min": 406,
        "max": 480,
        "range": 74
      },
      "crossline": {
        "min": 403,
        "max": 485,
        "range": 82
      }
    },
    "well_names": [
      "MJ-106",
      "MJ-115",
      "MJ-116",
      "MJ-119",
      "MJ-124",
      "MJ-128",
      "MJ-129",
      "MJ-130",
      "MJ-131",
      "MJ-133",
      "MJ-135",
      "MJ-136",
      "MJ-137",
      "MJ-138",
      "MJ-141",
      "MJ-142",
      "MJ-144",
      "MJ-145",
      "MJ-148",
      "MJ-149",
      "MJ-150",
      "MJ-151",
      "MJ-154",
      "MJ-155",
      "MJ-156",
      "MJ-157"
    ]
  }
}
```

---

### `GET /api/well/<string:well_name>`

**Purpose:** Retrieve details for a specific well by name.

**Path Parameters:**

| Parameter   | Type   | Description                    |
|-------------|--------|--------------------------------|
| `well_name` | string | The name of the well to fetch. |

**Query Parameters:**

| Parameter | Type   | Default                  | Description                          |
|-----------|--------|--------------------------|--------------------------------------|
| `dataset` | string | `well_coordinatesmj_B_G` | Name of the well dataset to query.   |

**Example Request:**

```bash
curl http://localhost:5000/api/well/MJ-106
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "inline": 480,
    "crossline": 403,
    "x": 342769.13,
    "y": 9694230.8,
    "trace_number": 15033,
    "bottom": 590.0,
    "bottom_reff": 295.0,
    "top": 418.0,
    "top_reff": 209.0,
    "well_x": 342772.48,
    "well_y": 9694232.43,
    "well_name": "MJ-106",
    "distance": 3.725506676
  }
}
```

**Error Response (Well Not Found):**

```json
{
  "success": false,
  "error": "Well 'MJ-999' not found in dataset 'well_coordinatesmj_B_G'"
}
```
HTTP Status: `404`

---

### `GET /api/well/<string:well_name>/exists`

**Purpose:** Check whether a well exists in the specified dataset.

**Path Parameters:**

| Parameter   | Type   | Description                     |
|-------------|--------|---------------------------------|
| `well_name` | string | The name of the well to check.  |

**Query Parameters:**

| Parameter | Type   | Default                  | Description                          |
|-----------|--------|--------------------------|--------------------------------------|
| `dataset` | string | `well_coordinatesmj_B_G` | Name of the well dataset to query.   |

**Example Request:**

```bash
curl http://localhost:5000/api/well/MJ-106/exists
```

**Example Response (Exists):**

```json
{
  "success": true,
  "data": {
    "exists": true
  }
}
```

**Example Response (Does Not Exist):**

```json
{
  "success": true,
  "data": {
    "exists": false
  }
}
```

---

### `GET /api/well/datasets`

**Purpose:** List all available well datasets.

**Query Parameters:** None

**Example Request:**

```bash
curl http://localhost:5000/api/well/datasets
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "datasets": [
      "well_coordinatesmj_B_G"
    ],
    "count": 1
  }
}
```

---

## Well Logs

Base path: `/api`

Well log endpoints are organized by log type: `phie`, `swe`, and `vsh`. Each log type supports the same five operations: listing all entries, listing well names, fetching data for a specific well, fetching TWT statistics for the log type, and fetching TWT statistics for a specific well.

> **Available Log Types:** `phie` (effective porosity), `swe` (water saturation), `vsh` (shale volume)

### `GET /api/well-log/<log_type>`

**Purpose:** Retrieve all well log entries of a specific type.

**Path Parameters:**

| Parameter  | Type   | Description                                    |
|------------|--------|------------------------------------------------|
| `log_type` | string | Log type: `phie`, `swe`, or `vsh`             |

**Query Parameters:**

| Parameter | Type   | Default   | Description                              |
|-----------|--------|-----------|------------------------------------------|
| `dataset` | string | `default` | Name of the well log dataset to query.   |

**Example Request:**

```bash
# Get all PHIE logs from default dataset
curl http://localhost:5000/api/well-log/phie

# Get all SWE logs
curl http://localhost:5000/api/well-log/swe

# Get all VSH logs
curl http://localhost:5000/api/well-log/vsh
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "wells": [
      {
        "well_name": "MJ-150",
        "log_type": "phie",
        "entries": [
          {"twt": 0.0, "value": 0.0032},
          {"twt": -2.0, "value": 0.0032},
          {"twt": -4.0, "value": 0.0032}
        ],
        "count": 2501
      },
      {
        "well_name": "MJ-151",
        "log_type": "phie",
        "entries": [
          {"twt": 0.0, "value": 0.16459},
          {"twt": -2.0, "value": 0.16459}
        ],
        "count": 2501
      }
    ],
    "count": 26
  }
}
```

**Error Response:**

```json
{
  "success": false,
  "error": "Dataset 'unknown' not found for log type 'phie'"
}
```
HTTP Status: `400`

---

### `GET /api/well-log/<log_type>/wells`

**Purpose:** Retrieve the list of well names that have data for a specific log type.

**Path Parameters:**

| Parameter  | Type   | Description                                    |
|------------|--------|------------------------------------------------|
| `log_type` | string | Log type: `phie`, `swe`, or `vsh`             |

**Query Parameters:**

| Parameter | Type   | Default   | Description                              |
|-----------|--------|-----------|------------------------------------------|
| `dataset` | string | `default` | Name of the well log dataset to query.   |

**Example Request:**

```bash
curl http://localhost:5000/api/well-log/phie/wells
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "well_names": [
      "MJ-106",
      "MJ-115",
      "MJ-116",
      "MJ-119",
      "MJ-124",
      "MJ-128",
      "MJ-129",
      "MJ-130",
      "MJ-131",
      "MJ-133",
      "MJ-135",
      "MJ-136",
      "MJ-137",
      "MJ-138",
      "MJ-141",
      "MJ-142",
      "MJ-144",
      "MJ-145",
      "MJ-148",
      "MJ-149",
      "MJ-150",
      "MJ-151",
      "MJ-154",
      "MJ-155",
      "MJ-156",
      "MJ-157"
    ],
    "count": 26
  }
}
```

---

### `GET /api/well-log/<log_type>/<string:well_name>`

**Purpose:** Retrieve well log data of a specific type for a single well.

**Path Parameters:**

| Parameter   | Type   | Description                                    |
|-------------|--------|------------------------------------------------|
| `log_type`  | string | Log type: `phie`, `swe`, or `vsh`             |
| `well_name` | string | The name of the well to fetch data for.        |

**Query Parameters:**

| Parameter | Type   | Default   | Description                              |
|-----------|--------|-----------|------------------------------------------|
| `dataset` | string | `default` | Name of the well log dataset to query.   |

**Example Request:**

```bash
curl http://localhost:5000/api/well-log/phie/MJ-150
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "well_name": "MJ-150",
    "log_type": "phie",
    "entries": [
      {"twt": 0.0, "value": 0.0032},
      {"twt": -2.0, "value": 0.0032},
      {"twt": -4.0, "value": 0.0032},
      {"twt": -6.0, "value": 0.0032}
    ],
    "count": 2501
  }
}
```

**Error Response (Well Not Found):**

```json
{
  "success": false,
  "error": "Well 'MJ-999' not found in PHIE log (dataset: 'default')"
}
```
HTTP Status: `404`

---

### `GET /api/well-log/<log_type>/stats`

**Purpose:** Retrieve TWT (Two-Way Time) statistics for a specific log type across all wells.

**Path Parameters:**

| Parameter  | Type   | Description                                    |
|------------|--------|------------------------------------------------|
| `log_type` | string | Log type: `phie`, `swe`, or `vsh`             |

**Query Parameters:**

| Parameter | Type   | Default   | Description                              |
|-----------|--------|-----------|------------------------------------------|
| `dataset` | string | `default` | Name of the well log dataset to query.   |

**Example Request:**

```bash
curl http://localhost:5000/api/well-log/phie/stats
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "log_type": "phie",
    "total_rows": 2501,
    "min_twt": -5000.0,
    "max_twt": 0.0,
    "max_abs_twt": 5000.0,
    "mid_twt": 2500.0
  }
}
```

**Error Response:**

```json
{
  "success": false,
  "error": "Dataset 'unknown' not found for log type 'phie'"
}
```
HTTP Status: `400`

---

### `GET /api/well-log/<log_type>/<string:well_name>/stats`

**Purpose:** Retrieve TWT (Two-Way Time) statistics for a specific well in a given log type, including the count of non-null values.

**Path Parameters:**

| Parameter   | Type   | Description                                    |
|-------------|--------|------------------------------------------------|
| `log_type`  | string | Log type: `phie`, `swe`, or `vsh`             |
| `well_name` | string | The name of the well to fetch statistics for.  |

**Query Parameters:**

| Parameter | Type   | Default   | Description                              |
|-----------|--------|-----------|------------------------------------------|
| `dataset` | string | `default` | Name of the well log dataset to query.   |

**Example Request:**

```bash
curl http://localhost:5000/api/well-log/phie/MJ-150/stats
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "well_name": "MJ-150",
    "log_type": "phie",
    "total_rows": 2501,
    "min_twt": -5000.0,
    "max_twt": 0.0,
    "max_abs_twt": 5000.0,
    "mid_twt": 2500.0,
    "non_null_count": 2501
  }
}
```

**Error Response (Well Not Found):**

```json
{
  "success": false,
  "error": "Well 'MJ-999' not found in PHIE log (dataset: 'default')"
}
```
HTTP Status: `404`

---

### `GET /api/well-log/datasets`

**Purpose:** List all available well log datasets and the log types each contains.

**Query Parameters:** None

**Example Request:**

```bash
curl http://localhost:5000/api/well-log/datasets
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "datasets": {
      "default": ["phie", "swe", "vsh"]
    },
    "count": 1
  }
}
```

---

## GNK Well Logs

Base path: `/api`

GNK well logs contain comprehensive petrophysical data (gamma ray, resistivity, density, neutron porosity, sonic, etc.) for GNK wells.

### `GET /api/well-log/gnk`

**Purpose:** Retrieve all GNK well log entries.

**Query Parameters:** None

**Example Request:**

```bash
curl http://localhost:5000/api/well-log/gnk
```

**Example Response:**

```json
{
  "success": true,
  "data": {
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
    "count": 934028
  }
}
```

---

### `GET /api/well-log/gnk/wells`

**Purpose:** Retrieve the list of well names available in the GNK well log.

**Query Parameters:** None

**Example Request:**

```bash
curl http://localhost:5000/api/well-log/gnk/wells
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "well_names": [
      "GNK-052",
      "GNK-053",
      "GNK-054"
    ],
    "count": 3
  }
}
```

---

### `GET /api/well-log/gnk/<string:well_name>`

**Purpose:** Retrieve all GNK well log entries for a specific well.

**Path Parameters:**

| Parameter   | Type   | Description                             |
|-------------|--------|-----------------------------------------|
| `well_name` | string | The name of the GNK well to fetch.      |

**Query Parameters:** None

**Example Request:**

```bash
curl http://localhost:5000/api/well-log/gnk/GNK-052
```

**Example Response:**

```json
{
  "success": true,
  "data": {
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
    "count": 15000
  }
}
```

**Error Response (Well Not Found):**

```json
{
  "success": false,
  "error": "Well 'GNK-999' not found in GNK well log"
}
```
HTTP Status: `404`

---

### `GET /api/well-log/gnk/count`

**Purpose:** Get the total count of all GNK well log entries across all wells.

**Query Parameters:** None

**Example Request:**

```bash
curl http://localhost:5000/api/well-log/gnk/count
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "total_entries": 934028
  }
}
```

---

## Horizons

Base path: `/api`

### `GET /api/horizon`

**Purpose:** Retrieve all horizon data points from a given dataset.

**Query Parameters:**

| Parameter | Type   | Default    | Description                           |
|-----------|--------|------------|---------------------------------------|
| `dataset` | string | `horizon`  | Name of the horizon dataset to query.   |

**Example Request:**

```bash
# Using default dataset
curl http://localhost:5000/api/horizon

# Using a specific dataset
curl "http://localhost:5000/api/horizon?dataset=MJ_FAR_coords"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "horizons": [
      {
        "X": 396028.0,
        "Y": 9625413.0,
        "Inline": 10001,
        "Crossline": 1270,
        "TraceNumber": 0,
        "bottom": 2000.702515,
        "bottom_reff": 1100.0,
        "top": 1357.939819,
        "top_reff": 779.0
      },
      {
        "X": 396039.0,
        "Y": 9625461.0,
        "Inline": 10001,
        "Crossline": 1272,
        "TraceNumber": 1,
        "bottom": 2000.702515,
        "bottom_reff": 1100.0,
        "top": 1357.939819,
        "top_reff": 779.0
      }
    ],
    "count": 393360
  }
}
```

**Error Response:**

```json
{
  "success": false,
  "error": "Failed to read horizon dataset 'unknown'"
}
```
HTTP Status: `500`

---

### `GET /api/horizon-page`

**Purpose:** Retrieve horizon data points with pagination support.

**Query Parameters:**

| Parameter   | Type    | Default    | Description                                 |
|-------------|---------|------------|---------------------------------------------|
| `dataset`   | string  | `horizon`  | Name of the horizon dataset to query.        |
| `page`      | integer | `1`        | Page number (1-indexed).                     |
| `page_size` | integer | `500`      | Number of items per page.                    |

**Example Request:**

```bash
# First page, default size
curl http://localhost:5000/api/horizon-page

# Second page with custom page size
curl "http://localhost:5000/api/horizon-page?page=2&page_size=100"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "horizons": [
      {
        "X": 396028.0,
        "Y": 9625413.0,
        "Inline": 10001,
        "Crossline": 1270,
        "TraceNumber": 0,
        "bottom": 2000.702515,
        "bottom_reff": 1100.0,
        "top": 1357.939819,
        "top_reff": 779.0
      }
    ],
    "count": 500
  }
}
```

---

### `GET /api/horizon/datasets`

**Purpose:** List all available horizon datasets.

**Query Parameters:** None

**Example Request:**

```bash
curl http://localhost:5000/api/horizon/datasets
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "datasets": [
      "horizon",
      "MJ_FAR_coords",
      "MJ_MID_coords"
    ],
    "count": 3
  }
}
```

---

## Image Helper

Base path: `/api`

### `GET /api/image-helper/<section_type>/<int:number>/dimensions`

**Purpose:** Retrieve the width and height dimensions of a seismic section image, along with its file path.

**Path Parameters:**

| Parameter      | Type    | Description                                                       |
|------------------|---------|-------------------------------------------------------------------|
| `section_type`   | string  | Type of section: `inline`, `crossline` |
| `number`         | integer | The section number.                                               |

**Query Parameters:**

| Parameter | Type   | Default   | Description                               |
|-----------|--------|-----------|-------------------------------------------|
| `dataset` | string | `default` | Name of the image dataset to query.         |

**Example Request:**

```bash
# Default dataset
curl http://localhost:5000/api/image-helper/crossline/505/dimensions

# Aster dataset
curl "http://localhost:5000/api/image-helper/inline/1067/dimensions?dataset=aster"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "section_type": "crossline",
    "section_number": 505,
    "width": 1200,
    "height": 800,
    "image_path": "csv_data/inline_crossline/default/crossline/crossline_505.png"
  }
}
```

**Error Response (Image Not Found):**

```json
{
  "success": false,
  "error": "Image for crossline 999 not found in dataset 'default'"
}
```
HTTP Status: `404`

**Error Response (Invalid Section Type):**

```json
{
  "success": false,
  "error": "Invalid section type 'invalid_type'"
}
```
HTTP Status: `400`

---

### `GET /api/image-helper/datasets`

**Purpose:** List all available image helper datasets and the section types each contains.

**Query Parameters:** None

**Example Request:**

```bash
curl http://localhost:5000/api/image-helper/datasets
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "datasets": {
      "default": ["inline", "crossline"],
      "aster": ["inline", "crossline"]
    },
    "count": 2
  }
}
```

---

## Seismic Sections

Base path: `/api`

These endpoints return raw PNG image data for seismic inline and crossline sections. The response is a binary `image/png` stream, not JSON.

### `GET /api/inline/<int:number>/image`

**Purpose:** Return a PNG image for the requested inline section number.

**Path Parameters:**

| Parameter | Type    | Description                |
|-----------|---------|----------------------------|
| `number`  | integer | The inline section number. |

**Query Parameters:**

| Parameter | Type   | Default   | Description                           |
|-----------|--------|-----------|---------------------------------------|
| `dataset` | string | `default` | Name of the seismic dataset to query.   |

**Example Request:**

```bash
# Save inline image to file
curl http://localhost:5000/api/inline/1067/image -o inline_1067.png

# Using aster dataset
curl "http://localhost:5000/api/inline/500/image?dataset=aster" -o inline_500.png
```

**Response Headers:**

```
Content-Type: image/png
Content-Length: 123456
Content-Disposition: inline; filename="inline_1067.png"
Cache-Control: public, max-age=3600
```

**Error Response (Section Not Found):**

```json
{
  "success": false,
  "error": "Inline section 999 not found in dataset 'default'"
}
```
HTTP Status: `404`

---

### `GET /api/crossline/<int:number>/image`

**Purpose:** Return a PNG image for the requested crossline section number.

**Path Parameters:**

| Parameter | Type    | Description                  |
|-----------|---------|------------------------------|
| `number`  | integer | The crossline section number.|

**Query Parameters:**

| Parameter | Type   | Default   | Description                           |
|-----------|--------|-----------|---------------------------------------|
| `dataset` | string | `default` | Name of the seismic dataset to query.   |

**Example Request:**

```bash
# Save crossline image to file
curl http://localhost:5000/api/crossline/505/image -o crossline_505.png
```

**Response Headers:**

```
Content-Type: image/png
Content-Length: 98765
Content-Disposition: inline; filename="crossline_505.png"
Cache-Control: public, max-age=3600
```

**Error Response:**

```json
{
  "success": false,
  "error": "Crossline section 999 not found in dataset 'default'"
}
```
HTTP Status: `404`

---

### `GET /api/seismic/datasets`

**Purpose:** List all available seismic datasets and the section types each contains.

**Query Parameters:** None

**Example Request:**

```bash
curl http://localhost:5000/api/seismic/datasets
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "datasets": {
      "default": ["inline", "crossline"],
      "aster": ["inline", "crossline"]
    },
    "count": 2
  }
}
```

---

### `GET /api/seismic/ranges`

**Purpose:** Retrieve the minimum, maximum, count, and range of available section numbers for each section type in a dataset.

**Query Parameters:**

| Parameter | Type   | Default   | Description                           |
|-----------|--------|-----------|---------------------------------------|
| `dataset` | string | `default` | Name of the seismic dataset to query.   |

**Example Request:**

```bash
# Default dataset
curl http://localhost:5000/api/seismic/ranges

# Specific dataset
curl "http://localhost:5000/api/seismic/ranges?dataset=aster"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "dataset": "default",
    "ranges": {
      "inline": {
        "min": 395,
        "max": 540,
        "count": 146,
        "range": 145
      },
      "crossline": {
        "min": 330,
        "max": 505,
        "count": 176,
        "range": 175
      }
    }
  }
}
```

**Error Response:**

```json
{
  "success": false,
  "error": "Unknown dataset 'unknown'. Available: ['aster', 'default']"
}
```
HTTP Status: `400`

---

## Appendix: Available Datasets Summary

| Resource        | Datasets                                                                 | Default              |
|-----------------|--------------------------------------------------------------------------|----------------------|
| Wells           | `well_coordinatesmj_B_G`                                                 | `well_coordinatesmj_B_G` |
| Well Logs       | `default`                                                                | `default`            |
| GNK Well Logs   | *(single dataset, path-based)*                                           | N/A                  |
| Horizons        | `horizon`, `MJ_FAR_coords`, `MJ_MID_coords`                              | `horizon`            |
| Image Helper    | `default`, `aster`                                                       | `default`            |
| Seismic Sections| `default`, `aster`                                                       | `default`            |
