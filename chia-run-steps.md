cd /nscratch/raghavgupta/fpga-port-flow
conda activate chia_env
source ~/create-ssh-agent.sh                                       
                                                                                
python -m chia.cli.main up cluster.yaml                                       
                                                                                                                                   
RAY_ADDRESS=a13:6380 chia job submit -- python /nscratch/raghavgupta/fpga-port-flow/fpga_port_flow.py
            
                                                                                                                                         
RAY_ADDRESS=a13:6380 ray job logs --follow $(RAY_ADDRESS=a13:6380 ray job list --format json 2>/dev/null | python3 -c "import sys,json; 
  jobs=json.load(sys.stdin); print(jobs[0]['submission_id'])")
# Dashboard at http://a13:8082                                                
                                                                            
# 4. Human review gates will block at:                                        
#    out/review/step_plan.json       → touch out/review/step_plan.approved    
#    out/review/step{N}_parts.json   → touch out/review/step{N}_parts.approved
                                                                            
# 5. Tear down when done                                                      
python -m chia.cli.main down cluster.yaml




RAY_ADDRESS=a13:6380 chia job submit -- python /nscratch/raghavgupta/fpga-port-flow/fpga_port_flow.py --resume-step 8 --resume-part 2 