
## API Reference

### Datasets

#### Get all datasets

```http
  GET /api/datasets
```
#### Upload new dataset

```http
  POST /api/datasets
```

#### Get specific dataset

```http
  GET /api/datasets/${id}
```

| Parameter | Type      | Description                       |
| :-------- | :-------  | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of item to fetch |

#### Full update of specific dataset

```http
  PUT /api/datasets/${id}
```

| Parameter | Type      | Description                       |
| :-------- | :-------  | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of item to fetch |

#### Partial update of specific dataset

```http
  PATCH /api/datasets/${id}
```

| Parameter | Type      | Description                       |
| :-------- | :-------  | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of item to fetch |

#### Delete specific dataset

```http
  DELETE /api/datasets/${id}
```

| Parameter | Type      | Description                       |
| :-------- | :-------  | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of item to fetch |


