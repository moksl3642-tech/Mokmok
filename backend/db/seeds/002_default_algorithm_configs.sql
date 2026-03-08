INSERT OR IGNORE INTO algorithm_configs (key, value, is_active) VALUES
  ('recommendation_model', '{"name": "hybrid-v1", "threshold": 0.75}', 1),
  ('difficulty_adjustment', '{"name": "bayesian", "window": 20}', 1),
  ('content_ranking', '{"name": "freshness-weighted", "alpha": 0.6}', 1);
