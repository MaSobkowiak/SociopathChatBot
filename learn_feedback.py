from chatterbot.conversation import Statement
"""
This example shows how to create a chat bot that
will learn responses based on an additional feedback
element from the user.
"""

def get_feedback():
    text = input()
    if 'yes' in text.lower():
        return True
    elif 'no' in text.lower():
        return False
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()

def training_with_feedback(bot):    
    while True:
        try:
            input_statement = Statement(text=input())
            response = bot.generate_response(
                input_statement
            )

            print('\n Is "{}" a coherent response to "{}"? \n'.format(
                response.text,
                input_statement.text
            ))

            if(get_feedback() is False):
                print('Please input the correct one:')
                correct_response = Statement(text=input())
                bot.learn_response(correct_response, input_statement)
                print('Responses added to bot!')
                print("--Type something to start learning--")

            elif(get_feedback() is True):
                print("--Type something to start learning--")

        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break