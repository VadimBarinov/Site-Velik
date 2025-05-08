from .database import get_db
from .load_data import LoadData
from .recommendations import Recommendations
import json

# когда буду делать api, переписать под async
def get_recommend(bike_id):
    db = get_db()

    load_data = LoadData()
    load_data.load_bikes_data(next(db))
    load_data.data_preparation()

    recommendations = Recommendations()
    recommendations.calc_recommendations(load_data.df, bike_id)

    return json.dumps(recommendations.recommend)