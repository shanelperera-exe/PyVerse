from flask import Flask, request
from random import randint

app = Flask(__name__)

# Generate the random number once when the app starts
random_number = randint(0, 9)

@app.route("/")
def guess():
    return """
        <h1 style="font-family: 'Poppins', sans-serif; text-align: center; margin-top: 50px;">GUESS THE NUMBER</h1>
        <h2 style="font-family: 'Courier New', Courier, monospace; text-align: center;">Guess a number between 0 and 9</h2>
        <img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" 
             alt="Guess a Number GIF" 
             style="display: block; margin: 20px auto; border: 5px solid black; border-radius: 15px;">
        <div style="text-align: center; margin-top: 20px;">
            <label for="number" style="font-family: 'Courier New', Courier, monospace; font-size: 18px; font-weight: bold;">Enter Number:</label>
            <form action="/guess" method="get" style="display: inline;">
                <input type="number" id="number" name="number" 
                       style="font-weight: bold; padding: 10px 15px; font-size: 18px; border: 2px solid #333; border-radius: 15px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); margin-top: 10px;" 
                       min="0" max="9">
                <button type="submit" 
                        style="font-family: 'Courier New', Courier, monospace; font-weight: bold; padding: 10px 20px; font-size: 18px; margin-left: 10px; background-color: #333; color: white; border: none; border-radius: 10px; cursor: pointer;">
                    Submit
                </button>
            </form>
        </div>
    """

@app.route("/guess")
def check_guess():
    user_guess = request.args.get("number", type=int)  # Get the number from the URL parameter

    if user_guess < random_number:
        message = """
            <div style="text-align: center; margin-top: 20px;">
                <h1 style="font-family: 'Courier New', Courier, monospace; color: red; font-weight: bold; text-align: center; margin-top: 20px;">Your guess is too low.</h1>
                <img src="https://y.yarn.co/5faf42af-cfa5-47c9-9de2-aab6b6d914d8_text.gif" 
                     alt="Guess a Number GIF" 
                     style="display: block; margin: 20px auto; border: 5px solid black; border-radius: 15px;">
                <a href="/" 
                   style="font-family: 'Courier New', Courier, monospace; font-weight: bold; text-align: center; font-size: 20px; color: white; background-color: black; padding: 10px 20px; border-radius: 10px; text-decoration: none; display: inline-block; margin-top: 20px;">
                   Try Again
                </a>
            </div>
        """
    elif user_guess > random_number:
        message = """
            <div style="text-align: center; margin-top: 20px;">
                <h1 style="font-family: 'Courier New', Courier, monospace; color: red; font-weight: bold;">Your guess is too high.</h1>
                <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzN5cmZzeHJpNzBpMjRncWg4MGZxb2NjOHVpaTg1aXFxMHh0OW50NyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/SyemapFxj7TiM/giphy.webp" 
                     style="display: block; margin: 20px auto; border: 5px solid black; border-radius: 15px;">
                <a href="/" 
                   style="font-family: 'Courier New', Courier, monospace; font-weight: bold; text-align: center; font-size: 20px; color: white; background-color: black; padding: 10px 20px; border-radius: 10px; text-decoration: none; display: inline-block; margin-top: 20px;">
                   Try Again
                </a>
            </div>
        """
    else:
        message = """
            <div style="text-align: center; margin-top: 20px;">
                <h1 style="font-family: 'Courier New', Courier, monospace; color: red; font-weight: bold;">Congratulations! You guessed it right!</h1>
                <img src="https://i.gifer.com/g0hA.gif" 
                     style="display: block; margin: 20px auto; border: 5px solid black; border-radius: 15px; width: 800px; height: 400px;">
            </div>
        """
    return message

if __name__ == "__main__":
    app.run(debug=True)
