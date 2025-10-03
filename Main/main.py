# Reading From the config file 
# Set up logger to write to a file, allows me to keep track what is happening 
# Store current positions in sql table, based on paper trading positions

# Start based on start time
    # Read articles from yahoo finance, 
        # Store the ticker and heading title
        # Feed to Finbert for a buy\sell\hold confidence number
    # Use confidence number and config thresholds to determine the action and how much money to put in or sell
    # Call alpaca paper trading api and put in the request

# End based on end time
