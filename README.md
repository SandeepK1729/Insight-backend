
## API Reference

### Datasets

#### Get all datasets

```https
  GET /api/datasets
```
#### Upload new dataset

```https
  POST /api/datasets
```

#### Get specific dataset

```https
  GET /api/datasets/${id}
```

| Parameter | Type      | Description                       |
| :-------- | :-------  | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of item to fetch |

#### Full update of specific dataset

```https
  PUT /api/datasets/${id}
```

| Parameter | Type      | Description                       |
| :-------- | :-------  | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of item to fetch |

#### Partial update of specific dataset

```https
  PATCH /api/datasets/${id}
```

| Parameter | Type      | Description                       |
| :-------- | :-------  | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of item to fetch |

#### Delete specific dataset

```https
  DELETE /api/datasets/${id}
```

| Parameter | Type      | Description                       |
| :-------- | :-------  | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of item to fetch |


