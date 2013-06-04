from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Module, current_app
import lib.auth


main = Module(__name__)
sageo = current_app

@main.route('/', methods=['GET'])
@lib.auth.login_required
def index():
    return render_template('main.html', page='dashboard')
