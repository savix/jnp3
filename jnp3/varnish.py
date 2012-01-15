# cache may be applied to functions which return HttpResponse objects
def cache(ttl):
    def decorated(raw_response):
        def new(self, *args, **kws):
            http_resp = raw_response(self, *args, **kws)
            http_resp._headers['x-varnish-ttl'] = ('X-Varnish-TTL', str(ttl))
            return http_resp
        return new
    return decorated
