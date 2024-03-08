import logging

def ConfigureCloudLogging():
        """ This function imports and configured the google cloud logging sdk """
        import google.cloud.logging
        # Instantiates a client
        client = google.cloud.logging.Client()
        client.setup_logging()
        logging.info("Using Cloud Loggging")