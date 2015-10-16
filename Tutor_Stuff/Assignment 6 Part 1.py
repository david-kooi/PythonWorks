def main():
    get_input()

def get_input():
    ROWS = int(input("Enter the number of rows (or -1 or -99 to quit): "))
    while ROWS != -1 and ROWS != -99:
        draw_pattern(ROWS)
        ROWS = int(input("\nEnter the number of rows (or -1 or -99 to quit): \n"))
    
def draw_pattern(ROWS):

        for var1 in range(ROWS):
            print("*")
            
            



main()
