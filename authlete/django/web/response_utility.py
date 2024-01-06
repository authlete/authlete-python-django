#
# Copyright (C) 2019-2024 Authlete, Inc.
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
    def okJson(cls, content, headers=None):
        # 200 OK, application/json;charset=UTF-8
        return cls.__json(200, content, headers)


    @classmethod
    def okJavaScript(cls, content, headers=None):
        # 200 OK, application/javascript;charset=UTF-8
        return cls.__javascript(200, content, headers)


    @classmethod
    def okJwt(cls, content, headers=None):
        # 200 OK, application/jwt
        return cls.__jwt(200, content, headers)


    @classmethod
    def okHtml(cls, content, headers=None):
        # 200 OK, text/html;charset=UTF-8
        return cls.__html(200, content, headers)


    @classmethod
    def entityStatement(cls, content, headers=None):
        # 200 OK, application/entity-statement+jwt
        return cls.__entityStatement(200, content, headers)


    @classmethod
    def created(cls, content, headers=None):
        # 201 Created, application/json;charset=UTF-8
        return cls.__json(201, content, headers)


    @classmethod
    def acceptedJson(cls, content, headers=None):
        # 202 Accepted, application/json;charset=UTF-8
        return cls.__json(202, content, headers)


    @classmethod
    def acceptedJwt(cls, content, headers=None):
        # 202 Accepted, application/jwt
        return cls.__jwt(202, content, headers)


    @classmethod
    def noContent(cls, headers=None):
        # 204 No Content
        return cls.__common(HttpResponse(status=204), headers)


    @classmethod
    def location(cls, location, headers=None):
        # 302 Found with a Location header.
        response = cls.__common(HttpResponse(status=302), headers)
        response['Location'] = location

        return response


    @classmethod
    def badRequest(cls, content, headers=None):
        # 400 Bad Request, application/json;charset=UTF-8
        return cls.__json(400, content, headers)


    @classmethod
    def unauthorized(cls, challenge, content=None, headers=None):
        # 401 Unauthorized with a WWW-Authenticate header
        return cls.wwwAuthenticate(401, challenge, content, headers)


    @classmethod
    def forbidden(cls, content, headers=None):
        # 403 Forbidden, application/json;charset=UTF-8
        return cls.__json(403, content, headers)


    @classmethod
    def notFound(cls, content, headers=None):
        # 404 Not Found, application/json;charset=UTF-8
        return cls.__json(404, content, headers)


    @classmethod
    def tooLarge(cls, content, headers=None):
        # 413 Too Large, application/json;charset=UTF-8
        return cls.__json(413, content, headers)


    @classmethod
    def internalServerError(cls, content, headers=None):
        # 500 Internal Server Error, application/json;charset=UTF-8
        return cls.__json(500, content, headers)


    @classmethod
    def wwwAuthenticate(cls, status, challenge, content=None, headers=None):
        if content is None:
            response = cls.__common(HttpResponse(status=status), headers)
        else:
            response = cls.__json(status, content, headers)

        response['WWW-Authenticate'] = challenge

        return response


    @classmethod
    def __response(cls, status, content, headers, content_type, charset='UTF-8'):
        response = HttpResponse(
            status=status, content=content,
            content_type=content_type, charset=charset)

        return cls.__common(response, headers)


    @classmethod
    def __common(cls, response, headers):
        response['Cache-Control'] = 'no-store'
        response['Pragma']        = 'no-cache'

        if headers is not None:
            for name, value in headers.items():
                response[ name ] = value

        return response


    @classmethod
    def __json(cls, status, content, headers):
        return cls.__response(status, content, headers, 'application/json')


    @classmethod
    def __javascript(cls, status, content, headers):
        return cls.__response(status, content, headers, 'application/javascript')


    @classmethod
    def __jwt(cls, status, content, headers):
        return cls.__response(status, content, headers, 'application/jwt', None)


    @classmethod
    def __html(cls, status, content, headers):
        return cls.__response(status, content, headers, 'text/html')


    @classmethod
    def __entityStatement(cls, status, content, headers):
        return cls.__response(status, content, headers, 'application/entity-statement+jwt')
