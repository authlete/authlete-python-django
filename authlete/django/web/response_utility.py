#
# Copyright (C) 2019 Authlete, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the
# License.


from django.http import HttpResponse


class ResponseUtility(object):
    @classmethod
    def okJson(cls, content):
        # 200 OK, application/json;charset=UTF-8
        return cls.__json(200, content)


    @classmethod
    def okJavaScript(cls, content):
        # 200 OK, application/javascript;charset=UTF-8
        return cls.__javascript(200, content)


    @classmethod
    def okJwt(cls, content):
        # 200 OK, application/jwt
        return cls.__jwt(200, content)


    @classmethod
    def okHtml(cls, content):
        # 200 OK, text/html;charset=UTF-8
        return cls.__html(200, content)


    @classmethod
    def noContent(cls):
        # 204 No Content
        return cls.__common(HttpResponse(status=204))


    @classmethod
    def location(cls, location):
        # 302 Found with a Location header.
        response = cls.__common(HttpResponse(status=302))
        response['Location'] = location

        return response


    @classmethod
    def badRequest(cls, content):
        # 400 Bad Request, application/json;charset=UTF-8
        return cls.__json(400, content)


    @classmethod
    def unauthorized(cls, challenge, content=None):
        # 401 Unauthorized with a WWW-Authenticate header
        return cls.wwwAuthenticate(401, challenge, content)


    @classmethod
    def forbidden(cls, content):
        # 403 Forbidden, application/json;charset=UTF-8
        return cls.__json(403, content)


    @classmethod
    def notFound(cls, content):
        # 404 Not Found, application/json;charset=UTF-8
        return cls.__json(404, content)


    @classmethod
    def internalServerError(cls, content):
        # 500 Internal Server Error, application/json;charset=UTF-8
        return cls.__json(500, content)


    @classmethod
    def wwwAuthenticate(cls, status, challenge, content=None):
        if content is None:
            response = cls.__common(HttpResponse(status=status))
        else:
            response = cls.__json(status, content)

        response['WWW-Authenticate'] = challenge

        return response


    @classmethod
    def __response(cls, status, content, content_type, charset='UTF-8'):
        response = HttpResponse(
            status=status, content=content,
            content_type=content_type, charset=charset)

        return cls.__common(response)


    @classmethod
    def __common(cls, response):
        response['Cache-Control'] = 'no-store'
        response['Pragma']        = 'no-cache'

        return response


    @classmethod
    def __json(cls, status, content):
        return cls.__response(status, content, 'application/json')


    @classmethod
    def __javascript(cls, status, content):
        return cls.__response(status, content, 'application/javascript')


    @classmethod
    def __jwt(cls, status, content):
        return cls.__response(status, content, 'application/jwt', None)


    @classmethod
    def __html(cls, status, content):
        return cls.__response(status, content, 'text/html')
