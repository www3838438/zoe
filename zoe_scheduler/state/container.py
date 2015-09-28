from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, PickleType

from zoe_scheduler.state import Base
from common.application_description import ZoeApplicationProcess


class ContainerState(Base):
    """
    :type id: int
    :type docker_id: str
    :type cluster_id: int
    :type ip_address: str
    :type readable_name: str
    :type description: ZoeApplicationProcess
    """
    __tablename__ = 'containers'

    id = Column(Integer, primary_key=True)
    docker_id = Column(String(128))
    cluster_id = Column(Integer, ForeignKey('clusters.id'))
    ip_address = Column(String(16))
    readable_name = Column(String(32))
    description = Column(PickleType())

    def to_dict(self) -> dict:
        ret = {
            'id': self.id,
            'docker_id': self.docker_id,
            'cluster_id': self.cluster_id,
            'ip_address': self.ip_address,
            'readable_name': self.readable_name,
            'description': self.description.to_dict()
        }

        return ret
