import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="indic-radar-gautam-db-99.mysql.database.azure.com",
        user="indic_admin",
        password="9369858652@Gg", 
        database="indic_radar_db"
    )
    return connection

def save_prediction_to_db(result_dict, user_id=1):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Step 4: Strict parameterized SQL Query 
    insert_query = """
    INSERT INTO predictions_logs 
    (user_id, input_headline, sentiment_score, sentiment_category, involved_countries, event_category, india_context_sentiment) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # Step 5: Data Formatting (Python List ko SQL friendly string mein badalna)

    # Tuple Mapping: Order strictly INSERT query ke columns jaisa hona chahiye
    data_tuple = (
        user_id,
        result_dict["headline_text"],
        result_dict["base_vader_score"],
        result_dict["base_vader_sentiment"],
        result_dict["entities_detected"],  
        result_dict["event_category"],
        result_dict["final_indic_sentiment"]
    )

    # Execution aur Commit
    cursor.execute(insert_query, data_tuple)
    connection.commit()

    # Memory leak se bachne ke liye connections close karna zaroori hai
    cursor.close()
    connection.close()