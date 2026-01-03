from logger import logging

def add(a,b):
    logging.debug("This Addition Operation is Taking Place")
    return a + b

logging.debug("The Addition function is called")
add(10,15)