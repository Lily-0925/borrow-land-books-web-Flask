from enum import Enum

class PendingStatus(Enum):
    #交易状态
    Waiting=0
    Success=1
    Reject=2
    Redraw=3

    @classmethod
    def pending_str(cls, status, key):
        key_map = {
            cls.Waiting: {
                'requester': 'Waiting for others to mail',
                'gifter': 'Waiting for you to mail'
            },
            cls.Reject: {
                'requester': 'gifter has rejected your request',
                'gifter': 'you have rejected the request'
            },
            cls.Redraw: {
                'requester': 'You have withdrawed this request',
                'gifter': 'gifter has withdrawed this request'
            },
            cls.Success: {
                'requester': 'gifter has mailed this book',
                'gifter': 'you have mailed this book'
            }
        }
        return key_map[status][key]