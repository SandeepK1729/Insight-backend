# Insight Backend

Insight Backend is the server-side component of the Insight machine learning web application. It provides a RESTful API for dataset management, model training, and prediction.

## Installation
To get started with Insight Backend, you'll need to clone this repository to your local machine and install its dependencies. Here's how to do that:

1. Clone the repository: `git clone https://github.com/SandeepK1729/insight-backend.git`
1. Change into the project directory: `cd insight-backend`
1. Install dependencies: `pip install -r requirements.txt`
1. Create .env file in Insight directory: 
   ```Python
      SECRET_KEY=<your-secret-key>
    ```
1. Change DATABASES in Insight/settings.py to LOCAL_DATABASE
1. Run migrations: `python manage.py migrate`
1. Start the server: `python manage.py runserver`

## Usage
Insight Backend provides a number of API endpoints for dataset management, model training, and prediction. 

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

To use Insight, you'll need to make requests to these endpoints using a client such as axios or fetch. You can also use the provided frontend application, which is available in the insight-frontend repository.

## Contributing
If you'd like to contribute to Insight Backend, you can fork the repository and submit a pull request with your changes. Please make sure that your changes are well-documented and tested before submitting a pull request.

## Credits
Insight Backend was built using the following technologies:

- Python
- Django
- Django REST Framework

## License
Insight Backend is released under the MIT License. Feel free to use, modify, and distribute the code however you like.
