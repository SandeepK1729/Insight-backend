
## API Reference

### Datasets

| Request   | Route                                     | Action                    			|
| :-------- | :-------                               	| :--------------------     			|			
| GET       | ```/api/datasets```                     	| Get all datasets          			|
| POST      | ```/api/datasets```                     	| Upload a dataset          			|
| GET       | ```/api/datasets/<int:dataset_id>```    	| Get a specific dataset				| 
| PUT       | ```/api/datasets/<int:dataset_id>```    	| Full update of specific dataset    	| 
| PATCH     | ```/api/datasets/<int:dataset_id>```    	| Partial update of specific dataset  	| 
| DELETE    | ```/api/datasets/<int:dataset_id>```    	| Delete specific dataset      			| 

### ModelFiles

| Request   | Route                               | Action                    			|
| :-------- | :-------                            | :--------------------     			|			
| GET       | ```/api/models```                   | Get all saved models          		|
| POST      | ```/api/models```                   | Train and save a model         		|
| GET       | ```/api/models/<int:model_id>```    | Get info of specific saved model	| 
| PUT       | ```/api/models/<int:model_id>```    | Modifies the specific saved model	| 
| PATCH     | ```/api/models/<int:model_id>```    | Modifies the specific saved model	| 
| DELETE    | ```/api/models/<int:model_id>```    | Delete specific saved model			| 

### Analyze report

| Request   | Route                              	| Action                    		|
| :-------- | :-------                              |:--------------------     			|			
| GET       | ```/api/analyze```                  	| Get metrics report of specific model with specific dataset_id if exist|
| POST      | ```/api/analyze```                  	| Get metrics report of specific model with specific dataset_id if exist else generate model and gives report|
