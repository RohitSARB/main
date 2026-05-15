# # 1-using a filehandler
# You can configure the logger to write logs to a file and then read the file to access the logged messages.
# import logging

# logging.basicConfig(
#     filename='logfile.log',
#     level=logging.DEBUG,
#     format="%(asctime)s-%(levelname)s-%(message)s"
# )

# logger = logging.getLogger()
# logger.info("This is an info message")
# logger.error("This is an error message")

# with open('logfile.log', 'r') as f:
#     log_content = f.read()

# print(log_content)



# 2-using stringIO in-memory logging
# If you don't want to write logs to a file, you can use Python's io.StringIO to capture logs in memory.
# import logging
# import io
# # Create an in-memory stream for logging
# log_stream = io.StringIO()
# stream_handler = logging.StreamHandler(log_stream)
# # Configure logger
# logger = logging.getLogger('memory_logger')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(stream_handler)
# # Log some messages
# logger.debug("Debug message")
# logger.warning("Warning message")
# # Access the log text from the stream
# log_content = log_stream.getvalue()
# print(log_content)



# 3. Using a Custom Logging Handler

# You can create a custom handler to capture log messages programmatically.

# import logging

# class CustomHandler(logging.Handler):
# def __init__(self):
# super().__init__()
# self.log_messages = []

# def emit(self, record):
# self.log_messages.append(self.format(record))

# # Configure logger with custom handler
# custom_handler = CustomHandler()
# formatter = logging.Formatter('%(levelname)s: %(message)s')
# custom_handler.setFormatter(formatter)

# logger = logging.getLogger('custom_logger')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(custom_handler)

# # Log some messages
# logger.info("Info message")
# logger.error("Error message")

# # Access logged messages
# print(custom_handler.log_messages)