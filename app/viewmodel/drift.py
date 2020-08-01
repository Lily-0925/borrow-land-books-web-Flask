from app.libs.enums import PendingStatus

class DriftCollection:
    def __init__(self, drifts, current_user_id):
        self.data = [DriftViewModel(drift, current_user_id).single_drift for drift in drifts]


class DriftViewModel:
    def __init__(self, drift,current_user_id):
        self.single_drift = self._parse(drift,current_user_id)

    def _parse(self,drift,current_user_id):
        a = "requester" if drift.requester_id == current_user_id else "gifter"
        pending_status=PendingStatus.pending_str(drift.pending, a)
        return {'drift_id': drift.id,
                'you_are': a,
                'book_title': drift.book_title,
                'book_author': drift.book_author,
                'book_img': drift.book_img,
                "date" : "",
                "operator": drift.gifter_nickname if
                drift.requester_id == current_user_id else drift.requester_nickname,
                'message': drift.message,
                'address': drift.address,
                'recipient_name':drift.recipient_name,
                'mobile': drift.mobile,
                'status': drift.pending,
                "status_str":pending_status
            }