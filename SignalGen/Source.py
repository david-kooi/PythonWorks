from audiogen import *
import sys


if __name__ == "__main__":

    audiogen.sampler.write_wav(sys.stdout, audiogen.tone(440))
    
    
