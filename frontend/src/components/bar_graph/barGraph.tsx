import { ChartContainer } from '@mui/x-charts/ChartContainer';
import { BarPlot } from '@mui/x-charts/BarChart';

const uData = [50, 30, 20, 27, 18, 23, 34, 50, 30, 20, 27, 18, 23, 34,];
const xLabels = [
  '13 Nov',
  '13 Nov',
  '13 Nov',
  '13 Nov',
  '13 Nov',
  '13 Nov',
  '13 Nov',
  '13 Nov',
  '13 Nov',
  '13 Nov',
  '13 Nov',
  '13 Nov',
  '13 Nov',
  '13 Nov',
  '13 Nov',
];


export default function TinyBarChart() {

  
  
  
  return (
    <ChartContainer
      width={500}
      height={300}
      series={[{ data: uData, label: 'uv', type: 'bar' }]}
      xAxis={[{ scaleType: 'band', data: xLabels }]}
    >
      <BarPlot />
    </ChartContainer>
  );
}
