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


class ClaimCollector(object):
    def __init__(self, subject, claimNames, claimLocales, claimProvider):
        """Constructor

        Args:
            subject (str)       : The subject (= unique identifier) of the user.
            claimNames (list)   : list of str. Claim names.
            claimLocales (list) : list of str. Claim locales.
            claimProvider (authlete.django.handler.spi.ClaimProviderSpi)
        """

        self._subject       = subject
        self._claimNames    = claimNames
        self._claimLocales  = self.__normalizeClaimLocales(claimLocales)
        self._claimProvider = claimProvider


    def __normalizeClaimLocales(self, claimLocales):
        if claimLocales is None or len(claimLocales) == 0:
            return None

        # From "5.2. Claims Languages and Scripts" in OpenID Connect Core 1.0
        #
        #   However, since BCP47 language tag values are case insensitive,
        #   implementations SHOULD interpret the language tag values supplied
        #   in a case insensitive manner.
        #

        localeList = list()
        localeSet  = set()
        for claimLocale in claimLocales:
            if claimLocale is None or len(claimLocale) == 0:
                continue

            locale = claimLocale.lower()
            if locale in localeSet:
                continue

            localeSet.add(locale)
            localeList.append(locale)

        if len(localeList) == 0:
            return None

        return localeList


    def collect(self):
        claimNames = self._claimNames

        if claimNames is None or len(claimNames) == 0:
            return None

        # Pairs of claim name and its value.
        collectedClaims = {}

        # For each required claim.
        for claimName in claimNames:
            if claimName is None:
                continue

            # Split the claim name into the name part and the language tag part.
            elements = claimName.split('#', 2)
            name = elements[0]
            tag  = None if len(elements) != 2 else elements[1]

            # If the name part is empty.
            if name is None or len(name) == 0:
                continue

            # Get the value of the claim.
            value = self.__getClaimValue(name, tag)

            # If the value of the claim was not obtained.
            if value is None:
                continue

            # Just for an edge case where claimName ends with '#'. e.g. 'family_name#'
            if tag is None or len(tag) == 0:
                claimName = name

            # Add the pair of the claim name and its value.
            collectedClaims[claimName] = value

        # If no claim value has been obtained.
        if len(collectedClaims) == 0:
            return None

        return collectedClaims


    def __getClaimValue(self, name, tag):
        provider = self._claimProvider
        subject  = self._subject

        # If a language tag is explicitly appended.
        if tag is not None and len(tag) != 0:
            # Get the claim value of the claim with the specific language tag.
            return provider.getUserClaimValue(subject, name, tag)

        # If claim locales are not specified by the 'claims_locales' parameter.
        if self._claimLocales is None:
            # Get the claim value of the claim without any language tag.
            return provider.getUserClaimValue(subject, name, None)

        # For each claim locale. They are ordered by preference.
        for locale in self._claimLocales:
            # Try to get the claim value with the claim locale.
            value = provider.getUserClaimValue(subject, name, locale)

            # If the claim value was obtained.
            if value is not None:
                return value

        # The last resort. Try to get the claim value without any language tag.
        return provider.getUserClaimValue(subject, name, None)
