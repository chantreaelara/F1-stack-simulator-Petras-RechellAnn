"""Flask Stack Simulator starter: complete TODOs during the live demo.
Before class, preview templates/index.html directly in the browser.
Running this file starts a status page, not the completed simulator.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import secrets
from queue_model import Queue

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    queue = Queue(session.get('queue', []))
    dequeued = session.get('dequeued', [])

    items = queue.items
    highlight = session.pop('highlight', False)

    return render_template(
        'index.html',
        items=items,
        size=queue.size(),
        dequeued=dequeued,
        front=queue.front(),
        rear=queue.rear(),
        highlight=highlight
    )


@app.route('/queue', methods=['POST'])
def operate():
    queue = Queue(session.get('queue', []))
    dequeued = session.get('dequeued', [])

    action = request.form.get('action', '').lower()
    value = request.form.get('value', '').strip()

    session['highlight'] = False

    if action == 'enqueue':
        if not value:
            flash('Please enter a value.', 'warning')
        elif len(value) > 24:
            flash('Value must not exceed 24 characters.', 'warning')
        elif queue.size() >= 20:
            flash('Queue is full. Maximum is 20 items.', 'warning')
        else:
            queue.enqueue(value)
            flash(f'{value} successfully added to the queue!', 'success')

    elif action == 'dequeue':
        if queue.is_empty():
            flash('Cannot dequeue. The queue is empty!', 'warning')
        else:
            removed = queue.dequeue()
            dequeued.append(removed)
            dequeued = dequeued[-20:]
            flash(f'Removed item: {removed}', 'success')

    elif action == 'peek':
        if queue.is_empty():
            flash('Cannot peek. The queue is empty!', 'warning')
        else:
            session['highlight'] = True
            flash(f'Front item: {queue.peek()}', 'info')

    elif action == 'clear':
        queue.clear()
        dequeued.clear()
        flash('Queue and removed items cleared!', 'success')

    else:
        flash('Invalid operation.', 'danger')

    session['queue'] = queue.items
    session['dequeued'] = dequeued

    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
