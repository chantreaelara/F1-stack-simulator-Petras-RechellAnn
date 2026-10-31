"""Flask Stack Simulator starter: complete TODOs during the live demo.
Before class, preview templates/index.html directly in the browser.
Running this file starts a status page, not the completed simulator.
"""

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash
)
import secrets
from stack_model import Stack

app = Flask(__name__)

# Secret key for session and flash messages
app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    # Restore stack values from session
    stack = Stack(session.get('stack', []))

    # Get removed items
    popped = session.get('popped', [])

    # Display stack from TOP to BOTTOM
    items = list(reversed(stack.items))

    # Check if top item should be highlighted
    highlight = session.pop('highlight', False)

    return render_template(
        'index.html',
        items=items,
        size=stack.size(),
        popped=popped,
        highlight=highlight
    )


@app.route('/stack', methods=['POST'])
def operate():
    # Restore stack and removed items
    stack = Stack(session.get('stack', []))
    popped = session.get('popped', [])

    # Get submitted form values
    action = request.form.get('action', '').lower()
    value = request.form.get('value', '').strip()

    # Reset highlight by default
    session['highlight'] = False

    if action == 'push':
        if not value:
            flash('Please enter a value.', 'warning')

        elif len(value) > 24:
            flash('Value must not exceed 24 characters.', 'warning')

        elif stack.size() >= 20:
            flash('Stack is full. Maximum is 20 items.', 'warning')

        else:
            stack.push(value)
            flash(f'{value} successfully pushed onto the stack!', 'success')

    elif action == 'pop':
        if stack.is_empty():
            flash('Cannot pop. The stack is empty!', 'warning')
        else:
            removed = stack.pop()
            popped.append(removed)

            # Keep only the latest 20 removed values
            popped = popped[-20:]

            flash(f'Removed item: {removed}', 'success')

    elif action == 'peek':
        if stack.is_empty():
            flash('Cannot peek. The stack is empty!', 'warning')
        else:
            session['highlight'] = True
            flash(f'Top item: {stack.peek()}', 'info')

    elif action == 'clear':
        stack.clear()
        popped.clear()
        flash('Stack and removed items cleared!', 'success')

    else:
        flash('Invalid operation.', 'danger')

    # Save updated values in session
    session['stack'] = stack.items
    session['popped'] = popped

    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
