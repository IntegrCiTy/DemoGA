within DHS.csBlocks;
model hpCentral

    parameter DHS.Types.ThermalDynamics thermalDynamicsIO = DHS.Types.ThermalDynamics.InitialOff;

    package Medium1 = Buildings.Media.Water(T_default=300);
    package Medium2 = Buildings.Media.Water(T_default=300);

    //////////////

    parameter Real eta=0.4;
    parameter Real etaEx=0.2;

    parameter Modelica.SIunits.Temperature Tin_cold=273+20 "K";
    parameter Modelica.SIunits.MassFlowRate mflow_in_cold=8 "kg/s";

    parameter Modelica.SIunits.Temperature Tin_hot=273+40 "K";
    parameter Modelica.SIunits.MassFlowRate mflow_in_hot=8 "kg/s";

    parameter Modelica.SIunits.Temperature Tout_hot_target=273+50 "K";

    Modelica.SIunits.Power Pelectric = hp.ht.P;
    Modelica.SIunits.Power Pthermal_in = hp.ht.Q2;
    Modelica.SIunits.Power Pthermal_out = hp.ht.Q1;

    Modelica.SIunits.Temperature Tout_cold = hp.ht.staB2.T;
    Modelica.SIunits.Temperature Tout_hot = hp.ht.staB1.T;

    ///////////////


    DHS.Subnetworks.BasicBlocks.heatPump hp (
        redeclare package MediumA = Medium2, 
        redeclare package MediumB = Medium1,
        redeclare DHS.HeatTransfer.Carnot_Tpi ht,
        hpMode = DHS.Types.HPmode.Heating, 
        thermalDynamics1= thermalDynamicsIO,
        thermalDynamics2=thermalDynamicsIO,
        eta=eta,
        etaEx=etaEx,
        tau1=1,
        tau2=1,
        m1_flow_nominal=10,
        m2_flow_nominal=10
        );

    DHS.Subnetworks.BasicBlocks.source_sink lake( redeclare package Medium = Medium2, 
        source(T=Tin_cold, m_flow=mflow_in_cold ) );


 DHS.Subnetworks.BasicBlocks.source_sink interface ( redeclare package Medium = Medium1, 
        source(T=Tin_hot, m_flow=mflow_in_hot ), 
        sourcestrand1=false);


    
Modelica.Blocks.Sources.Constant T_target( k=Tout_hot_target );

    
equation
    connect(lake.lport, hp.lport_A);
    connect(hp.lport_B, interface.lport);

    connect(T_target.y, hp.ht.Ttarget);

end hpCentral;