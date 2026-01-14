from backend.config import API_ENDPOINTS, ROLE
from backend.database import engine
from backend.models import Accessibility, Endpoint, Role
from backend.modules import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


# Create role of app
def getReadyRole():
    checkRole = session.query(Role).all()

    # check role db have role if not then add role
    if len(checkRole) == 0:
        roleObjList = []
        for role, roleId in ROLE().roles.items():
            roleObjList.append(Role(id=roleId, role=role))

        session.add_all(roleObjList)
        session.commit()
        session.close()

    # _______________ Add initial endpoints
    checkEndpoint = session.query(Endpoint).all()
    # check role db have role if not then add role
    if len(checkEndpoint) == 0:
        endpointObjList = []
        for endpoint, routeAccess in API_ENDPOINTS().apiEndpoints.items():
            endpointObjList.append(
                Endpoint(endpoint=endpoint, methods=routeAccess.methods)
            )

        session.add_all(endpointObjList)
        session.commit()
        session.close()

    # _______________
    # Add accessibility in database
    checkAccessibility = session.query(Accessibility).all()

    # check role db have role if not then add role
    if len(checkAccessibility) == 0:
        accessObjList = []
        for role_id, routeAccess in enumerate(API_ENDPOINTS().apiEndpoints.values()):
            accessObjList.append(
                Accessibility(
                    endpointID=role_id + 1,
                    roles=routeAccess.rolePermission,
                    partialAccess=routeAccess.partialAccess,
                )
            )

        session.add_all(accessObjList)
        session.commit()
        session.close()
