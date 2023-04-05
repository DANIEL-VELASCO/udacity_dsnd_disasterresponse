import sys
import pandas as pd
import sqlalchemy
import sqlite3


def load_data(messages_filepath, categories_filepath):
    """Takes in the messages file path (messages_filepath ) and the categories file path (categories_filepath) and combines them to cerate a new dataset"""
    
    # load messages dataset
    messages = pd.read_csv(messages_filepath)
    # load categories dataset
    categories = pd.read_csv(categories_filepath)
    # Merge the messages and categories datasets using the common id
    df = messages.merge(categories, on="id", how='left')    
    
    return df



def clean_data(df):
    """This function perform some text cleaning and normalization """
    
    # Split the values in the categories column on the ;  character
    categories = df['categories'].str.split(';',expand=True)

    # Select the first row of the categories dataframe
    row = categories.iloc[0].tolist()

    # Extract a list of new column names for categories.
    category_colnames = [col[:len(col) - 2] for col in row]
    
    # rename the columns of `categories`
    categories.columns = category_colnames

    # Convert category values to just numbers 0 or 1
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].str[-1]
        # convert column from string to numeric
        categories[column] = categories[column].astype(int)
    
    # Replace categories column in df with new category columns.
    df = df.drop(columns=['categories'])
    
    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis=1)

    # drop duplicates
    df = df.drop_duplicates(keep='first')

    return df


    
def save_data(df, database_filename):
    """This function saves the data into a sqlite database"""  
    
    # Save the clean dataset into an sqlite database
    engine = sqlalchemy.create_engine('sqlite:///'+database_filename)
    
    # connect to the database
    conn = sqlite3.connect(database_filename)
    
    # get a cursor
    cur = conn.cursor()
    
    # drop the test table in case it already exists
    cur.execute("DROP TABLE IF EXISTS real_life_disasters")

    #save db
    df.to_sql('real_life_disasters', engine, index=False)  


def main():
    
    
    if len(sys.argv) == 4:
        print('entro')
        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()