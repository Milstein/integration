__author__ = "Basheeruddin Ahmed"
__copyright__ = "Copyright(c) 2014, Cisco Systems, Inc."
__license__ = "New-style BSD"
__email__ = "syedbahm@cisco.com"
import sys
import UtilLibrary
import SettingsLibrary

#
#Creates the specified number of cars based on Cars yang model
# using RESTCONF
#

def addCar(hostname,port,numberOfCars):

    for x in range(1, numberOfCars+1):
        strId = str(x)
        payload = SettingsLibrary.add_car_payload_template.substitute(id=strId,category="category"+strId,model="model"+strId,
                                                           manufacturer="manufacturer"+strId,
                                                           year=(2000+x%100))
        print("payload formed after template substitution=")
        print(payload)
        # Send the POST request
        resp = UtilLibrary.post(SettingsLibrary.getAddCarUrl(hostname,port),"admin", "admin",payload)

        print("the response of the POST to add car=")
        print(resp)

    return resp

    #TBD: Detailed validation


#
#Creates the specified number of persons based on People yang model
# using main RPC
# <note>
#   To enable RPC a non-user input person entry is created with personId=user0
# </note>
#
def addPerson(hostname,port,numberOfPersons):
    #FOR RPC TO WORK PROPERLY THE FIRST ENTRY SHOULD BE VIA RESTCONF
    if(numberOfPersons==0):
        strId =str(numberOfPersons)
        payload = SettingsLibrary.add_person_payload_template.substitute(personId="user"+strId,gender="unknown",age=0,
                                                                  address=strId + "Way, Some Country, Some Zip  "+strId,
                                                                  contactNo= "some number"+strId)
        # Send the POST request using RESTCONF
        resp = UtilLibrary.nonprintpost(SettingsLibrary.getAddPersonUrl(hostname,port),"admin", "admin",payload)
        return resp

    genderToggle = "Male"
    for x in range(1, numberOfPersons+1):
        if(genderToggle == "Male"):
            genderToggle = "Female"
        else:
            genderToggle = "Male"

        strId = str(x)

        payload = SettingsLibrary.add_person_rpc_payload_template.substitute(personId="user"+strId,gender=genderToggle,age=(20+x%100),
                                                                      address=strId + "Way, Some Country, Some Zip  "+str(x%1000),
                                                                      contactNo= "some number"+strId)
        # Send the POST request using RPC
        resp = UtilLibrary.post(SettingsLibrary.getAddPersonRpcUrl(hostname,port),"admin", "admin",payload)

        print("payload formed after template substitution=")
        print(payload)
        print("the response of the POST to add person=")
        print(resp)

    return resp


    #TBD: Detailed validation

#This method is not exposed via commands as only getCarPersons is of interest
#addCarPerson entry happens when buyCar is called
# <note>
#   To enable RPC a non-user input car-person entry is created with personId=user0
# </note>
#
def addCarPerson(hostname,port,numberOfCarPersons):

    #FOR RPC TO WORK PROPERLY THE FIRST ENTRY SHOULD BE VIA RESTCONF
    if(numberOfCarPersons==0):
        payload = SettingsLibrary.add_car_person_template.substitute(Id=str(numberOfCarPersons),personId="user"+str(numberOfCarPersons))
        # Send the POST request REST CONF
        resp = UtilLibrary.nonprintpost(SettingsLibrary.getAddCarPersonUrl(hostname,port),"admin", "admin",payload)

        return

    for x in range(1, numberOfCarPersons+1):
        strId = str(x)

        payload = SettingsLibrary.add_car_person_template.substitute(Id=strId,personId="user"+strId)

        # Send the POST request REST CONF
        resp = UtilLibrary.post(SettingsLibrary.getAddCarPersonUrl(hostname,port),"admin", "admin",payload)

        print("payload formed after template substitution=")
        print(payload)

        print("the response of the POST to add car_person=")
        print(resp)

    print("getting the car_persons for verification")
    resp=getCarPersonMappings(hostname,port,0)

    #TBD detailed validation

#
# Invokes an RPC REST call that does a car purchase by a person id
# <note>
# It is expected that the Car and Person entries are already created
# before invoking this method
# </note>
#

def buyCar(hostname,port,numberOfCarBuyers):
    for x in range(1, numberOfCarBuyers+1):
        strId = str(x)

        payload = SettingsLibrary.buy_car_rpc_template.substitute(personId="user"+strId,carId=strId)

        # Send the POST request using RPC
        resp = UtilLibrary.post(SettingsLibrary.getBuyCarRpcUrl(hostname,port),"admin", "admin",payload)

        print("payload formed after template substitution=")
        print(payload)

        print("the response of the POST to buycar=")
        print(resp)

    print("getting the car_persons for verification")
    resp=getCarPersonMappings(hostname,port,0)


#
# Uses the GET on car:cars resource
# to get all cars in the store using RESTCONF
#
#
def getCars(hostname,port,ignore):
    resp = UtilLibrary.get(SettingsLibrary.getCarsUrl(hostname,port),"admin", "admin")
    resp.encoding = 'utf-8'
    print (resp.text)
    return resp

#
# Uses the GET on people:people resource
# to get all persons in the store using RESTCONF
#<note>
#This also returns the dummy entry created for routed RPC
# with personId being user0
#</note>
#
#
def getPersons(hostname,port,ignore):
    resp = UtilLibrary.get(SettingsLibrary.getPersonsUrl(hostname,port),"admin","admin")
    resp.encoding = 'utf-8'
    print (resp.text)
    return resp

#
# Uses the GET on car-people:car-people resource
# to get all car-persons entry in the store using RESTCONF
#<note>
#This also returns the dummy entry created for routed RPC
# with personId being user0
#</note>
#
def getCarPersonMappings(hostname,port,ignore):
    resp = UtilLibrary.get(SettingsLibrary.getCarPersonUrl(hostname,port),"admin","admin")
    resp.encoding = 'utf-8'
    print (resp)

    return resp

#
#delete all cars in the store using RESTCONF
#
#
def deleteAllCars(hostname,port,ignore):
    UtilLibrary.delete(SettingsLibrary.getCarsUrl(hostname,port),"admin","admin")
    resp = getCars(hostname,port,ignore)
    print("Cars in store after deletion:"+ str(resp))

#
#delete all persons in the store using RESTCONF
#
#
def deleteAllPersons(hostname,port,ignore):
    UtilLibrary.delete(SettingsLibrary.getPersonsUrl(hostname,port),"admin","admin")
    resp = getPersons(hostname,port,ignore)
    print("Persons in store after deletion:"+ str(resp))


#
#delete all car -poeple s in the store using RESTCONF
#
#
def deleteAllCarsPersons(hostname,port,ignore):
    UtilLibrary.delete(SettingsLibrary.getCarPersonsUrl(hostname,port),"admin","admin")
    resp = getPersons(hostname,port,ignore)
    print("Persons in store after deletion:"+ str(resp))

#
# Usage message shown to user
#

def options():

    command = 'ac=Add Car\n\t\tap=Add Person \n\t\tbc=Buy Car\n\t\tgc=Get Cars\n\t\tgp=Get Persons\n\t\t' \
              'gcp=Get Car-Person Mappings\n\t\tdc=Delete All Cars\n\t\tdp=Delete All Persons)'

    param =  '\n\t<param> is\n\t\t' \
             'number of cars to be added if <command>=ac\n\t\t' \
             'number of persons to be added if <command>=ap\n\t\t' \
             'number of car buyers if <command>=bc\n\t\t'\
             'pass 0 if <command>=gc or gp or gcp or dc or dp'\


    usageString = 'usage: python crud <ipaddress> <command> <param>\nwhere\n\t<ipaddress> = ODL server ip address' \
                  '\n\t<command> = any of the following commands \n\t\t'

    usageString = usageString + command +param

    print (usageString)


#
# entry point for command executions
#

def main():
    if len(sys.argv) < 4:
        options()
        quit(0)
    SettingsLibrary.hostname = sys.argv[1]
    SettingsLibrary.port = '8181'
    call = dict(ac=addCar, ap=addPerson, bc=buyCar,
                gc=getCars, gp=getPersons, gcp=getCarPersonMappings,dc=deleteAllCars,dp=deleteAllPersons)

    #FOR RPC TO WORK PROPERLY THE FIRST PERSON SHOULD BE ADDED VIA RESTCONF
    addPerson(SettingsLibrary.hostname,SettingsLibrary.port,0)

    #FOR RPC TO WORK PROPERLY THE FIRST PERSON SHOULD BE ADDED VIA RESTCONF
    addCarPerson(SettingsLibrary.hostname,SettingsLibrary.port,0)


    call[sys.argv[2]](SettingsLibrary.hostname,SettingsLibrary.port,int(sys.argv[3]))

#
# main invoked
if __name__ == "__main__":
 main()
