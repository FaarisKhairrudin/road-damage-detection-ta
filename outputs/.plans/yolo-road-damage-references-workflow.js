return await runs.all([
  { key: "models", agent: "researcher", task: "Read outputs/.plans/yolo-road-damage-references-T1.md and write outputs/.drafts/yolo-road-damage-references-research-models.md.", output: "outputs/.drafts/yolo-road-damage-references-research-models.md" },
  { key: "domain", agent: "researcher", task: "Read outputs/.plans/yolo-road-damage-references-T2.md and write outputs/.drafts/yolo-road-damage-references-research-domain.md.", output: "outputs/.drafts/yolo-road-damage-references-research-domain.md" },
  { key: "loss", agent: "researcher", task: "Read outputs/.plans/yolo-road-damage-references-T3.md and write outputs/.drafts/yolo-road-damage-references-research-loss.md.", output: "outputs/.drafts/yolo-road-damage-references-research-loss.md" },
  { key: "efficiency", agent: "researcher", task: "Read outputs/.plans/yolo-road-damage-references-T4.md and write outputs/.drafts/yolo-road-damage-references-research-efficiency.md.", output: "outputs/.drafts/yolo-road-damage-references-research-efficiency.md" },
]);
