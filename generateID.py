#import random library for psudeo-random number generation
import random

def generateID() :
    #set constant beginning to ID sequence
    INIT = "VCC"

    #seeding a random number using system date and time
    random.seed()

    #generate and return patient ID number 
    return INIT + f"{random.randint(100,10000)}"