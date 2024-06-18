from typing import Required, TypedDict

from dixa.api import DixaResource, DixaVersion
from dixa.exceptions import DixaAPIError
from dixa.model.v1.anonymization import AnonymizationRequest
from dixa.model.v1.conversation import Conversation, ConversationTypes
from dixa.model.v1.end_user import (
    EndUser,
    EndUserCustomAttribute,
    EndUserPatchBulkActionOutcome,
    EndUserPatchBulkActionOutcomes,
)


class EndUserCreateBody(TypedDict, total=False):
    additionalEmails: list[str]
    additionalPhoneNumbers: list[str]
    avatarUrl: str
    displayName: str
    email: str
    externalId: str
    firstName: str
    lastName: str
    middleNames: list[str]
    phoneNumber: str


class EndUserListQuery(TypedDict, total=False):
    email: str
    externalId: str
    phone: str


class EndUserPatchBody(TypedDict, total=False):
    additionalEmails: list[str]
    additionalPhoneNumbers: list[str]
    avatarUrl: str
    displayName: str
    email: str
    externalId: str
    firstName: str
    lastName: str
    middleNames: list[str]
    phoneNumber: str


# Implement as dict[str, str | list[str]]
type EndUserPatchCustomAttributesBody = dict[str, str | list[str]]


class EndUserPatchBulkBody(TypedDict, total=False):
    additionalEmails: list[str]
    additionalPhoneNumbers: list[str]
    avatarUrl: str
    displayName: str
    email: str
    externalId: str
    firstName: str
    id: Required[str]
    lastName: str
    middleNames: list[str]
    phoneNumber: str


class EndUserUpdateBody(TypedDict, total=False):
    additionalEmails: list[str]
    additionalPhoneNumbers: list[str]
    avatarUrl: str
    displayName: str
    email: str
    externalId: str
    firstName: str
    lastName: str
    middleNames: list[str]
    phoneNumber: str


class EndUserUpdateBulkBody(TypedDict, total=False):
    additionalEmails: list[str]
    additionalPhoneNumbers: list[str]
    avatarUrl: str
    displayName: str
    email: str
    externalId: str
    firstName: str
    id: Required[str]
    lastName: str
    middleNames: list[str]
    phoneNumber: str


class EndUserResource(DixaResource):
    """
    https://docs.dixa.io/openapi/dixa-api/v1/tag/End-Users/
    """

    resource = "endusers"
    dixa_version: DixaVersion = "v1"

    def anonymize(self, end_user_id: str) -> AnonymizationRequest:
        """Anonymize an end user.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/End-Users/#tag/End-Users/operation/patchEndusersUseridAnonymize
        """
        data = self.client.patch(f"{self._url}/{end_user_id}/anonymize")
        if not isinstance(data, dict):
            raise DixaAPIError(f"Expected dict, got {type(data).__name__}")
        return AnonymizationRequest(**data)

    def create(self, body: EndUserCreateBody) -> EndUser:
        """Create an end user.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/End-Users/#tag/End-Users/operation/postEndusers
        """
        data = self.client.post(self._url, body)
        if not isinstance(data, dict):
            raise DixaAPIError(f"Expected dict, got {type(data).__name__}")
        return EndUser(**data)

    def create_bulk(
        self, body: list[EndUserCreateBody]
    ) -> list[EndUserPatchBulkActionOutcome]:
        """Create end users.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/End-Users/#tag/End-Users/operation/postEndusersBulk
        """
        data = self.client.post(f"{self._url}/bulk", {"data": body}, list)
        if not isinstance(data, list):
            raise DixaAPIError(f"Expected list, got {type(data).__name__}")

        results = []
        for elem in data:
            for return_cls in EndUserPatchBulkActionOutcomes:
                try:
                    results.append(return_cls(**elem))
                    break
                except TypeError:
                    continue
            else:
                raise DixaAPIError(
                    f"Expected one of {EndUserPatchBulkActionOutcomes}, got {type(data).__name__}"
                )

        return results

    def get(self, end_user_id: str) -> EndUser:
        """Get an end user by id.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/End-Users/#tag/End-Users/operation/getEndusersUserid
        """
        data = self.client.get(f"{self._url}/{end_user_id}")
        if not isinstance(data, dict):
            raise DixaAPIError(f"Expected dict, got {type(data).__name__}")
        return EndUser(**data)

    def list_conversations(self, end_user_id: str) -> list[Conversation]:
        """List conversations.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/End-Users/#tag/End-Users/operation/getEndusersUseridConversations
        """
        data = self.client.paginate(f"{self._url}/{end_user_id}/conversations")
        if not isinstance(data, list):
            raise DixaAPIError(f"Expected list, got {type(data).__name__}")
        for return_cls in ConversationTypes:
            try:
                return return_cls(**data[0])
            except TypeError:
                continue
        else:
            raise DixaAPIError(
                f"Expected one of {ConversationTypes}, got {type(data).__name__}"
            )

    def list_(self, query: EndUserListQuery | None = None) -> list[EndUser]:
        """List end users.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/End-Users/#tag/End-Users/operation/getEndusers
        """
        return self.client.paginate(self._url, query)

    def patch(self, end_user_id: str, body: EndUserPatchBody) -> EndUser:
        """Patch an end_user.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/End-Users/#tag/End-Users/operation/patchEndusersUserid
        """
        data = self.client.patch(f"{self._url}/{end_user_id}", body)
        if not isinstance(data, dict):
            raise DixaAPIError(f"Expected dict, got {type(data).__name__}")
        return EndUser(**data)

    def patch_end_user_custom_attributes(
        self, end_user_id: str, body: EndUserPatchCustomAttributesBody
    ) -> list[EndUserCustomAttribute]:
        """Patch end user custom attributes.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/End-Users/#tag/End-Users/operation/patchEndusersUseridCustom-attributes
        """
        data = self.client.patch(
            f"{self._url}/{end_user_id}/custom-attributes", body, list
        )
        if not isinstance(data, list):
            raise DixaAPIError(f"Expected dict, got {type(data).__name__}")
        return [EndUserCustomAttribute(**attribute) for attribute in data]

    def patch_bulk(
        self, body: list[EndUserPatchBulkBody]
    ) -> list[EndUserPatchBulkActionOutcome]:
        """Patch end users.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/End-Users/#tag/End-Users/operation/patchEndusers
        """
        data = self.client.patch(self._url, {"data": body}, list)
        if not isinstance(data, list):
            raise DixaAPIError(f"Expected list, got {type(data).__name__}")
        results = []
        for elem in data:
            for return_cls in EndUserPatchBulkActionOutcomes:
                try:
                    results.append(return_cls(**elem))
                    break
                except TypeError:
                    continue
            else:
                raise DixaAPIError(
                    f"Expected one of {EndUserPatchBulkActionOutcomes}, got {type(data).__name__}"
                )

        return results

    def update(self, end_user_id, body: EndUserUpdateBody) -> EndUser:
        """Update an end user.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/End-Users/#tag/End-Users/operation/putEndusersUserid
        """
        data = self.client.put(f"{self._url}/{end_user_id}", body)
        if not isinstance(data, dict):
            raise DixaAPIError(f"Expected dict, got {type(data).__name__}")
        return EndUser(**data)

    def update_bulk(
        self, body: list[EndUserUpdateBulkBody]
    ) -> list[EndUserPatchBulkActionOutcome]:
        """Update an end users.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/End-Users/#tag/End-Users/operation/putEndusers
        """
        data = self.client.put(self._url, {"data": body}, list)
        if not isinstance(data, list):
            raise DixaAPIError(f"Expected list, got {type(data).__name__}")
        results = []
        for elem in data:
            for return_cls in EndUserPatchBulkActionOutcomes:
                try:
                    results.append(return_cls(**elem))
                    break
                except TypeError:
                    continue
            else:
                raise DixaAPIError(
                    f"Expected one of {EndUserPatchBulkActionOutcomes}, got {type(data).__name__}"
                )

        return results
