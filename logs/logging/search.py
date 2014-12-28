
class Search(object):

    def search_logs(self, profile, max_results=0, search=''):
        log_list = []
        if search:
            log_list = profile.logs.filter(name__istartswith=search)
        else:
            log_list = profile.logs.all()

        if max_results > 0 and len(log_list) > max_results:
            log_list = log_list[:max_results]
        return log_list
