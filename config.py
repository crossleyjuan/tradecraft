import inject

from da import ReviewDA

def configure():
    def config(binder):

        binder.bind(ReviewDA, ReviewDA())

    inject.configure(config)
