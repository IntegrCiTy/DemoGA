within DHS.csBlocks;
model threeDoublePipesNode

    //////////////

    parameter Modelica.SIunits.Temperature T0_in=273+30 "K";
    parameter Modelica.SIunits.Temperature Th_in=273+15 "K";
    parameter Modelica.SIunits.Temperature Tc_in=273+45 "K";

    parameter Modelica.SIunits.MassFlowRate mflow0_in=5 "kg/s";
    parameter Modelica.SIunits.MassFlowRate mflowh_in=8 "kg/s";
    parameter Modelica.SIunits.MassFlowRate mflowc_in=3 "kg/s";

    parameter Modelica.SIunits.Length length_pipes_0 = 100 "m";
    parameter Modelica.SIunits.Length diameter_pipes_0 = 0.2 "m";

    parameter Modelica.SIunits.Length length_pipes_h = 100 "m";
    parameter Modelica.SIunits.Length diameter_pipes_h = 0.2 "m";

    parameter Modelica.SIunits.Length length_pipes_c = 100 "m";
    parameter Modelica.SIunits.Length diameter_pipes_c = 0.2 "m";

    Modelica.SIunits.Temperature T0_out= sta0_out.T;
    Modelica.SIunits.Temperature Th_out= stah_out.T;
    Modelica.SIunits.Temperature Tc_out= stac_out.T;

protected

    package Medium = Buildings.Media.Water;

    Medium.ThermodynamicState sta0_out = Medium.setState_phX( interface_0.lport[2].p, 
                                                            inStream(interface_0.lport[2].h_outflow), 
                                                            inStream(interface_0.lport[2].Xi_outflow));
    Medium.ThermodynamicState stah_out = Medium.setState_phX( interface_h.lport[1].p, 
                                                            inStream(interface_h.lport[1].h_outflow), 
                                                            inStream(interface_h.lport[1].Xi_outflow));
    Medium.ThermodynamicState stac_out = Medium.setState_phX( interface_c.lport[2].p, 
                                                            inStream(interface_c.lport[2].h_outflow), 
                                                            inStream(interface_c.lport[2].Xi_outflow));

    ///////////////

    DHS.Subnetworks.BasicBlocks.doublePipe pipes_0( 
        redeclare package Medium = Medium , 
        pipeType = DHS.Types.PipeType.idealTransport , 
        length=length_pipes_0, 
        pipe_diameter=diameter_pipes_0
    );
    DHS.Subnetworks.BasicBlocks.doublePipe pipes_h( 
        redeclare package Medium = Medium , 
        pipeType = DHS.Types.PipeType.idealTransport , 
        length=length_pipes_h, 
        pipe_diameter=diameter_pipes_h
    );
    DHS.Subnetworks.BasicBlocks.doublePipe pipes_c( 
        redeclare package Medium = Medium , 
        pipeType = DHS.Types.PipeType.idealTransport , 
        length=length_pipes_c, 
        pipe_diameter=diameter_pipes_c
    );

    DHS.Subnetworks.BasicBlocks.valve_serial valve (
        redeclare package Medium = Medium,
        valve(m_flow=mflowc_in),
        strand1=false
    );

    DHS.Subnetworks.BasicBlocks.source_sink interface_0 ( redeclare package Medium = Medium, 
        source(T=T0_in, m_flow=mflow0_in )
        );
    DHS.Subnetworks.BasicBlocks.source_sink interface_h ( redeclare package Medium = Medium, 
        source(T=Th_in, m_flow=mflowh_in ),
        source_on_strand1=false
        );
    DHS.Subnetworks.BasicBlocks.source_sink interface_c ( redeclare package Medium = Medium, 
        source(T=Tc_in, m_flow=mflowc_in )
        );

    
equation

    connect(interface_0.lport, pipes_0.lport_A);
    connect(pipes_0.lport_B, pipes_h.lport_A);
    connect(pipes_h.lport_B, interface_h.lport);

    connect(pipes_0.lport_B, pipes_c.lport_A);
    connect(pipes_c.lport_B, valve.lport_A);
    connect(valve.lport_B, interface_c.lport);
    
end threeDoublePipesNode;