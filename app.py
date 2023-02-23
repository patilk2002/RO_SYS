# importing Flask and other modules
from flask import Flask, request, render_template

# Flask constructor
app = Flask(__name__)

# A decorator used to tell the application
# which URL is associated function

result = [[]]



    
@app.route('/', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        # getting input form HTML form

        vol = request.form.get("vol")
        vol2 = request.form.get("vol2")

        num=request.form.get("elements") 
        N=float(num)# Number of elements in one pressure vessel
        print("\n",N)
        A = request.form.get("temperature")
        B = request.form.get("flowfact")

        T = float(A)
        F = float(B)
        # variables inputs from the form
        # T = 25.0  # Temperature degree Celsius
        # F = 0.85  # Flow Factor

        Cf = 35000.0  # mg / l # Feedwater concentration mg/L
        Qf = 0.000333333  # Feedwater flow rate m3/s

        # N = 4.0  # Number of elements in one pressure vessel

        # Main Program
        import math
        import numpy as np
        pi = math.pi
        # Input Membrane Parameters

        print("Input Membrane Parameters")
        Sm = 37.2  # Single element Membrane Area m2
        L = 0.965  # Lenght of membrane element m
        b = 0.85  # Width of membrane element m
        df = 0.00033  # Filament Thk m
        lm = 0.00327  # Mesh Length m
        h = 0.0006  # Spacer Thk m
        theta = 105.0  # Spacer Angle (deg)
        n = 28.0  # No. of envelopes in a element
        # Pure water permeability coefficient at 25 degrees m3/(m2.kg/m.s2)
        A25 = 0.000000000000293333
        B25 = 0.00000000293333  # Solute permeability coefficient at 25 degrees m/s
        # T = 25.0  # Temperature degree Celsius
        # F = 0.85  # Flow Factor
        Klambda = 2.4  # Pressure vessels and module fittings losses in pressure

        """## Input Feedwater Characteristics"""
        print("Input Feedwater Characteristics")
        Cf = 35000.0  # mg / l # Feedwater concentration mg/L
        Qf = 0.000333333  # Feedwater flow rate m3/s
        """## Input Membrane Configuration of entire RO System
        
        ## Calculations
        """
        print("Input Membrane Configuration of entire RO System")
        # N = 4.0  # Number of elements in one pressure vessel
        NPv = 1.0  # Number of pressure vessels in one stage
        Am = Sm * N * NPv  # Total Membrane Area in the entire RO System m2
        VSP = 0.5 * pi * df**2 * lm  # Volume of Spacer m3
        Vtotal = lm**2 * math.sin(math.radians(theta))*h  # Total Volume m3
        porocity = (1-(VSP/Vtotal))  # Porosity
        term1 = (1-porocity)*(4/df)
        term2 = (2/h)
        term3 = 4*porocity

        result.clear()
        # Hydraulic Diameter for Spiral Wound membrane m
        dh = term3 / (term2+term1)
        print('total membrane area in m2 is', Am)
        print('volume of spacer in m3', VSP)
        print('total volume in m3', Vtotal)
        print('porocity is ', porocity)
        print('value of dh is ', dh)

        """Calculation for Entire RO plant"""

        R = 0.32  # Assumed Recovery of Entire RO plant
        print('feedwater concentation:', Cf)
        print('feedflow rate:', Cf)
        OSMFeed = 79.94 * Cf  # Feedwater Osmotic Pressure kg/m.s2
        Cc = (Cf / (1-R))  # Concentrate Concentration mg/L
        # Average Feed and Concentrate water Concentration mg/L
        Cfc = ((2-R)/(2-(2*R)))*Cf
        print('concentrate cocentration:', Cc)
        Qp = Qf * R  # Permeate Flow rate m3/s
        Qc = Qf - Qp  # Concentrate Flow rate m3/s
        Qb = (Qf+Qc)/2  # Average Feed and Concentrate Flow rate m3/s
        Vfb = Qb/(b*h*porocity*n)  # Average Feed Concentrate Flow rate m/s
        # Average Feed and Concentrate water Concentration Moles
        M = Cfc/(10000)
        # Density of Average Feed and Concentrate water kg/m3
        rho = (((3*10**(-5))*M**2)+(0.0069*M)+0.9972)*1000
        # Dynamic Viscosity of Average Feed and Concentrate water kg/m.s
        Mu = (1.234*10**(-6))*math.exp((0.0212*(Cfc*0.001))+(1965/(273.15+T)))
        Re = (rho*Vfb*dh)/(Mu)  # Reynolds Number
        Lambda = (Klambda*6.23*Re**(-0.3))  # Empirical Friction Factor
        # Pressure drop at the feed side of a Spiral Wound Module kg/ms2
        DeltaPfb = (Lambda*L*rho*Vfb**2)/(2*dh)
        CF = Cfc/Cf  # Concentration Factor
        D = (6.275*10**(-6))*math.exp(((0.1546*10**(-3))*Cfc) -
                                      (2513/(273.15+T)))  # Solute Diffusivity m2/s
        Sc = Mu/(rho*D)  # Schmidt Number
        k = 0.065*(D/dh)*(Re**(0.875))*Sc**(0.25)  # Mass Transfer Coefficient
        Jw = Qp/Am  # Permeate Water Flux m3/m2.s
        CP = float(math.exp(Jw/k))  # Concentration Polarization Factor
        PiM = CF*CP*OSMFeed  # Osmotic pressure on the membrane surface kg/m.s2
        # Permeate water concentration mg/L
        Cp = B25*CP*(Am/Qp)*((Cf*(1+CF))/2)
        PiP = 79.94*Cp  # Osmotic pressure of permeate water kg/m.s2
        DeltaPi = PiM-PiP  # Osmotic pressure gradient kg/m.s2
        # applied Hydraulic Pressure to the RO system kg/m.s2
        PfT = (Qp/((A25)*Am))+(DeltaPi)+(DeltaPfb/2)
        print('value of PfT for entire RO plant is', PfT)
        # Calculated Permeate water flow rate m3/s
        Qpcal = A25*((PfT-(DeltaPfb/2))-(DeltaPi))*Am
        Rcal = Qpcal/Qf  # Calculated Recovery of RO system
        print('value of Rcal for entire RO plant is', Rcal)
        R1 = R
        """## Iteration"""

        for NPv in range(1, int(NPv)+1):
            print('for ', NPv, 'pressure vessle :')
            for N in range(1, int(N)+1):

                print('For ', N, 'Element')
                for i in np.arange(0.000001, R, 0.000001):

                    R1 = i
                    #Cp = (Cf/R) *(1-math.pow((1-R1),(1-Rej)))
                    #Cc = Cf*(math.pow((1-R1),(-Rej)))
                    #R =((Cc-Cf)/(Cc-Cp))
                    #print('feedwater concentation:',Cf)
                    #print('feedflow rate:',Cf)
                    OSMFeed = 79.94 * Cf  # Feedwater Osmotic Pressure kg/m.s2
                    Cc = (Cf / (1-R1))  # Concentrate Concentration mg/L
                    # Average Feed and Concentrate water Concentration mg/L
                    Cfc = ((2-R1)/(2-(2*R1)))*Cf
                    #print('concentrate cocentration:',Cc)
                    Qp = Qf * R1  # Permeate Flow rate m3/s
                    Qc = Qf - Qp  # Concentrate Flow rate m3/s
                    # Average Feed and Concentrate Flow rate m3/s
                    Qb = (Qf+Qc)/2
                    # Average Feed Concentrate Flow rate m/s
                    Vfb = Qb/(b*h*porocity*n)
                    # Average Feed and Concentrate water Concentration Moles
                    M = Cfc/(10000)
                    # Density of Average Feed and Concentrate water kg/m3
                    rho = (((3*10**(-5))*M**2)+(0.0069*M)+0.9972)*1000
                    # Dynamic Viscosity of Average Feed and Concentrate water kg/m.s
                    Mu = (1.234*10**(-6)) * \
                        math.exp((0.0212*(Cfc*0.001))+(1965/(273.15+T)))
                    Re = (rho*Vfb*dh)/(Mu)  # Reynolds Number
                    # Empirical Friction Factor
                    Lambda = (Klambda*6.23*Re**(-0.3))
                    # Pressure drop at the feed side of a Spiral Wound Module kg/ms2
                    DeltaPfb = (Lambda*L*rho*Vfb**2)/(2*dh)
                    CF = Cfc/Cf  # Concentration Factor
                    D = (6.275*10**(-6))*math.exp(((0.1546*10**(-3))*Cfc) -
                                                  (2513/(273.15+T)))  # Solute Diffusivity m2/s
                    Sc = Mu/(rho*D)  # Schmidt Number
                    # Mass Transfer Coefficient
                    k = 0.065*(D/dh)*(Re**(0.875))*Sc**(0.25)
                    Jw = Qp/Sm  # Permeate Water Flux m3/m2.s
                    # Concentration Polarization Factor
                    CP = float(math.exp(Jw/k))
                    PiM = CF*CP*OSMFeed  # Osmotic pressure on the membrane surface kg/m.s2
                    # Permeate water concentration mg/L
                    Cp = B25*CP*(Sm/Qp)*((Cf*(1+CF))/2)
                    PiP = 79.94*Cp  # Osmotic pressure of permeate water kg/m.s2
                    DeltaPi = PiM-PiP  # Osmotic pressure gradient kg/m.s2
                    # applied Hydraulic Pressure to the RO system kg/m.s2
                    PfTcal = (Qp/((A25)*Sm))+(DeltaPi)+(DeltaPfb/2)
                    #print('value of PfT is',PfT)
                    # Calculated Permeate water flow rate m3/s
                    Qpcal = A25*((PfT-(DeltaPfb/2))-(DeltaPi))*Sm
                    Rcal = Qpcal/Qf  # Calculated Recovery of RO system

                    if (abs(R1-Rcal) < 1e-05):
                        r = []
                        print('Results for', NPv,
                              'pressule vessle &', N, 'element')
                        r.append(Rcal)
                        print('value of Rcal is', Rcal)

                        print('feed water Characteristics:')
                        r.append(Qf)
                        r.append(Cf)
                        print('value of Qf :', Qf, 'm3/s')
                        print('value of Cf :', Cf, 'mg/l')

                        print('Concentrate water characteristics:')
                        r.append(Qc)
                        r.append(Cc)
                        print('value of Qc:', Qc, 'm3/s')
                        print('value of Cc :', Cc, 'mg/l')

                        print('Permeate water characteristics:')
                        r.append(Cp)
                        r.append(Qpcal)
                        r.append(Vfb)
                        print('value of Cp:', Cp, 'mg/l')
                        print('value of Qp :', Qpcal, 'm3/s')
                        print('value of Vfb :', Vfb, 'm/s')

                        print('Other parameters :')
                        r.append(Vfb)
                        r.append(Qb)
                        r.append(Mu)
                        r.append(Re)
                        r.append(D)
                        r.append(Sc)
                        r.append(k)
                        r.append(Jw)
                        r.append(CP)

                        print('value of Avg feed brine velocity(Vfb):', Vfb, 'm/s')
                        print('value oF Avg feed brine flow rate (Qb):', Qb, 'm3/s')
                        print('value of Dynamic viscosity (mu):', Mu, 'kg/ms')
                        print('value of Reynolds number (Re):', Re)
                        print('value of Solute diffusivity (D):', D, 'm2/s')
                        print('value of Schmidt Number (Sc):', Sc)
                        print('value of Mass Transfer coefficient (K):', k)
                        print('value of Permeate Water Flux (Jw):', Jw, 'm3/m2*s')
                        print('value of Concentratio Polarization (CP):', CP)

                        print('pressure parameters:')
                        r.append(PfT)
                        r.append(DeltaPfb)
                        r.append(PiM)
                        r.append(PiP)
                        r.append(DeltaPi)

                        print('value of feed water pressure (P) :', PfT, 'kg/ms2')
                        print('value of pressure drop at feed side (deltaP):',
                              DeltaPfb, 'kg/ms2')
                        print(
                            'value of osmotic pressure on membrane surface(pi M):', PiM, 'kg/ms2')
                        print('value of permeate osmotic pressure (pi P):',
                              PiP, 'kg/ms2')
                        print('value of osmotic pressure gradient (delta pi) :',
                              DeltaPi, 'kg/ms2')

                        Cf = Cc
                        Qf = Qc
                        PfT = round(PfT, 2)
                        DeltaPfb = round(DeltaPfb, 2)
                        PfT = PfT + (- DeltaPfb)
                        result.append(r)
        
        total_recovery=1-((1-result[0][0])*((1-result[1][0]))*(1-result[2][0])*(1-result[3][0]))
        total=1
        for i in range(int(N)):
            total*=(1-result[i][0])

        total=1-total;
        # for i in range(4):
            # print(i)
            # print(result)
            # print(result[i][6])
            # result[i][6]=round(result[i][6],4)

            # # result[i][8]=round(result[i][8],4)


            # print(result[i][6])

            # total_recovery*=(1-result[i][0])
                            
            # total_recovery=1-total_recovery

        result.append([total])

        print("********************************************\n\n", T, F, N, total)
        return render_template("overall.html", result=result)
        # return "<div style='text-align:center;height:100px;width:500px;padding:50px 100px;border:2px solid;border-radius:10px;margin:0 auto;margin-top:200px;'><h2>The Alkalinity is : "+str(120)+" mg/L of CaCO3 </h2></div>"

    return render_template("index.html", result=result)



if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
