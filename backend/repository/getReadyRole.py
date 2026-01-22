from backend.config import API_ENDPOINTS, ROLE
from backend.database import engine
from backend.models import Accessibility, Category, Endpoint, Role
from backend.modules import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


# Create role of app
def getReadyRole():
    checkRole = session.query(Role).all()

    # Check if db has role or not then add role
    if len(checkRole) == 0:
        roleObjList = []
        for role, roleId in ROLE().roles.items():
            roleObjList.append(Role(id=roleId, role=role))

        session.add_all(roleObjList)
        session.commit()
        session.close()

    # _______________ Add initial endpoints
    checkEndpoint = session.query(Endpoint).all()
    # Check if db has endpoints or not then add
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

    # check if db has accessibility or not then add
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

    # _______________
    checkCategory = session.query(Category).all()

    # Check if db has categories or not then add
    if len(checkCategory) == 0:
        catObjList = []
        for category in [
            "Politcs",
            "Reletable",
            "Troll",
            "Coding",
            "Programming",
            "Movies",
            "Sad",
            "Casual",
            "Trending",
        ]:
            catObjList.append(Category(category=category))

        session.add_all(catObjList)
        session.commit()
        session.close()
