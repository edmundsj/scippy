For some reason, my Siglent SDG1025 was once found by pyvisa, but now is not
being found by pyvisa using rm.list_resources(). AHA. It looks like it just
takes awhile to boot up. I now see the instrument listed as 
USB0::0xF4ED::0xEE3A::SDG10GA3163315::INSTR
The read termination appears to be \r\n and the write termination is just \n. 
It is now responding to my queries.
