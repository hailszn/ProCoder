'''list='part,sku,brand_code,make,model,year,partterminologyname,notes,qty,mfrlabel,position,aspiration,bedlength,bedtype,block,bodynumdoors,bodytype,brakeabs,brakesystem,cc,cid,cylinderheadtype,cylinders,drivetype,enginedesignation,enginemfr,engineversion,enginevin,frontbraketype,frontspringtype,fueldeliverysubtype,fueldeliverytype,fuelsystemcontroltype,fuelsystemdesign,fueltype,ignitionsystemtype,liters,mfrbodycode,rearbraketype,rearspringtype,region,steeringsystem,steeringtype,submodel,transmissioncontroltype,transmissionmfr,transmissionmfrcode,transmissionnumspeeds,transmissiontype,valvesperengine,wheelbase'
list = list.split(",")

print(list)

for i in list:
    print (f"final_unique['{i}'] = ''")

for i in list:
    print (f"'{i}',", end='')'''

list2 = 'sku,part,item_id,brand_code,make,model,year,partterminologyname,notes,qty,mfrlabel,position,aspiration,bedlength,bedtype,block,bodynumdoors,bodytype,brakeabs,brakesystem,cc,cid,cylinderheadtype,cylinders,drivetype,enginedesignation,enginemfr,engineversion,enginevin,frontbraketype,frontspringtype,fueldeliverysubtype,fueldeliverytype,fuelsystemcontroltype,fuelsystemdesign,fueltype,ignitionsystemtype,liters,mfrbodycode,rearbraketype,rearspringtype,region,steeringsystem,steeringtype,submodel,transmissioncontroltype,transmissionmfr,transmissionmfrcode,transmissionnumspeeds,transmissiontype,valvesperengine,wheelbase'
list2 = list2.split(',')
for i in list2:
    print(f"final_unique['{i}'] = ''")

for i in list2:
    print(f"'{i}',",end='')