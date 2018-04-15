/* I made a mistake with barebones_pso and alternative_barebones_pso. This deletes those results... */

DELETE FROM diversity WHERE pso_name = 'alternative_barebones_pso';
DELETE FROM diversity WHERE pso_name = 'barebones_pso';

DELETE FROM droc WHERE pso_name = 'alternative_barebones_pso';
DELETE FROM droc WHERE pso_name = 'barebones_pso';

DELETE FROM droc_rank_between_psos WHERE pso_1_name = 'alternative_barebones_pso';
DELETE FROM droc_rank_between_psos WHERE pso_1_name = 'barebones_pso';
DELETE FROM droc_rank_between_psos WHERE pso_2_name = 'alternative_barebones_pso';
DELETE FROM droc_rank_between_psos WHERE pso_2_name = 'barebones_pso';
